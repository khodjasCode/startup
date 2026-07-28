# Telegram qismi (aiogram 3, long polling)
# Ishga tushirish:  python -m bot.main

import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command

from bot.config import BOT_TOKEN
from bot.rag import (
    javob_olish,
    collection,
    TokenlarTugadi,
    TOKENLAR_TUGADI_XABARI_TARJIMALARI,
    XATOLIK_XABARI_TARJIMALARI,
)
from bot.index_qurish import bazani_yuklash

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Har bir chat uchun suhbat tarixi (aniqlashtiruvchi savol-javob oqimi uchun).
# MVP uchun xotirada saqlanadi; bot qayta ishga tushsa tarix yo'qoladi.
SUHBAT_TARIXI: dict[int, list[dict]] = {}
TARIX_UZUNLIGI = 8  # so'nggi N ta xabar (fuqaro+bot) saqlanadi

# Har bir chat uchun tanlangan javob tili — /start da tugma orqali tanlanadi,
# tanlanmasa (masalan, foydalanuvchi to'g'ridan-to'g'ri savol yozib yuborsa)
# o'zbek tili standart bo'lib qoladi.
FOYDALANUVCHI_TILI: dict[int, str] = {}
TIL_NOMLARI = {"uz": "O'zbekcha", "ru": "Русский", "en": "English"}
QIDIRYAPMAN_XABARI = {"uz": "Qidiryapman... ⏳", "ru": "Ищу... ⏳", "en": "Searching... ⏳"}
TIL_TANLANDI_XABARI = {
    "uz": "✅ Til: O'zbekcha tanlandi.",
    "ru": "✅ Язык: выбран русский.",
    "en": "✅ Language: English selected.",
}


def til_klaviaturasi() -> types.InlineKeyboardMarkup:
    tugmalar = [
        [types.InlineKeyboardButton(text=nom, callback_data=f"til:{kod}")]
        for kod, nom in TIL_NOMLARI.items()
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=tugmalar)


@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "Assalomu alaykum! Men davlat xizmatlari bo'yicha yo'naltiruvchi botman.\n\n"
        "Muammoingizni oddiy tilda yozing (masalan: «3 kundan beri suv kelmayapti»), "
        "men qaysi idoraga qanday murojaat qilishni aytaman.\n\n"
        "⚠️ Men huquqiy maslahat bermayman — faqat yo'naltiraman.\n\n"
        "🌐 Javob tilini tanlang / Выберите язык ответов / Choose your reply language:",
        reply_markup=til_klaviaturasi(),
    )


@dp.callback_query(F.data.startswith("til:"))
async def til_tanlandi(call: types.CallbackQuery):
    til = call.data.split(":", 1)[1]
    FOYDALANUVCHI_TILI[call.message.chat.id] = til
    await call.answer()
    await call.message.edit_text(TIL_TANLANDI_XABARI.get(til, TIL_TANLANDI_XABARI["uz"]))


@dp.message()
async def savol(msg: types.Message):
    til = FOYDALANUVCHI_TILI.get(msg.chat.id, "uz")
    await msg.answer(QIDIRYAPMAN_XABARI.get(til, QIDIRYAPMAN_XABARI["uz"]))

    tarix = SUHBAT_TARIXI.setdefault(msg.chat.id, [])
    tarix.append({"rol": "fuqaro", "matn": msg.text})

    try:
        javob = javob_olish(tarix, til)
        tarix.append({"rol": "bot", "matn": javob})
        del tarix[:-TARIX_UZUNLIGI]
    except TokenlarTugadi:
        javob = TOKENLAR_TUGADI_XABARI_TARJIMALARI.get(til, TOKENLAR_TUGADI_XABARI_TARJIMALARI["uz"])
        tarix.pop()  # foydalanuvchi savoli javobsiz qoldi, tarixga qo'shilmasin
    except Exception as e:
        javob = XATOLIK_XABARI_TARJIMALARI.get(til, XATOLIK_XABARI_TARJIMALARI["uz"])
        print("XATO:", e)
    await msg.answer(javob)


if __name__ == "__main__":
    # Indeks bo'sh bo'lsagina qayta quramiz — har startda 300+ yozuvni
    # qayta indekslash bir necha daqiqa olib, botni kechiktiradi.
    # Baza yangilanganda qo'lda: python3 -m bot.index_qurish
    if collection.count() == 0:
        print("Vektor baza bo'sh — indekslanmoqda...", flush=True)
        bazani_yuklash()
    print("Bot ishga tushdi, polling boshlandi.", flush=True)
    asyncio.run(dp.start_polling(bot))
