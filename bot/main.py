# Telegram qismi (aiogram 3, long polling)
# Ishga tushirish:  python -m bot.main

import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command

from baza import suhbat
from bot.config import BOT_TOKEN
from bot.rag import (
    javob_olish,
    vektorlar_soni,
    TokenlarTugadi,
    TOKENLAR_TUGADI_XABARI_TARJIMALARI,
    XATOLIK_XABARI_TARJIMALARI,
)
from bot.index_qurish import bazani_yuklash

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Suhbat tarixi va tanlangan til Postgres'da saqlanadi (`baza/suhbat.py`) —
# bot qayta ishga tushsa ham ular joyida qoladi. Baza chaqiruvlari bloklovchi,
# shuning uchun ular `asyncio.to_thread` orqali alohida oqimda bajariladi.

# Tanlangan javob tili /start dagi tugma orqali belgilanadi; tanlanmasa
# (masalan, foydalanuvchi to'g'ridan-to'g'ri savol yozib yuborsa) o'zbekcha.
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
    await asyncio.to_thread(suhbat.telegram_tilini_saqlash, call.message.chat.id, til)
    await call.answer()
    await call.message.edit_text(TIL_TANLANDI_XABARI.get(til, TIL_TANLANDI_XABARI["uz"]))


@dp.message()
async def savol(msg: types.Message):
    til = await asyncio.to_thread(suhbat.telegram_tili, msg.chat.id)
    await msg.answer(QIDIRYAPMAN_XABARI.get(til, QIDIRYAPMAN_XABARI["uz"]))

    # Bazadagi tarix + shu savol. Bazaga savol javob bilan birga yoziladi:
    # javobsiz qolgan savol keyingi so'rovga noto'g'ri kontekst bermasligi kerak.
    tarix = await asyncio.to_thread(suhbat.tarix, msg.chat.id, suhbat.TELEGRAM)
    tarix.append({"rol": "fuqaro", "matn": msg.text})

    try:
        javob = javob_olish(tarix, til)
        await asyncio.to_thread(
            suhbat.saqlash, msg.chat.id, msg.text, javob, til, suhbat.TELEGRAM
        )
    except TokenlarTugadi:
        javob = TOKENLAR_TUGADI_XABARI_TARJIMALARI.get(til, TOKENLAR_TUGADI_XABARI_TARJIMALARI["uz"])
    except Exception as e:
        javob = XATOLIK_XABARI_TARJIMALARI.get(til, XATOLIK_XABARI_TARJIMALARI["uz"])
        print("XATO:", e)
    await msg.answer(javob)


if __name__ == "__main__":
    # Indeks bo'sh bo'lsagina qayta quramiz — har startda 300+ yozuvni
    # qayta indekslash bir necha daqiqa olib, botni kechiktiradi.
    # Baza yangilanganda qo'lda: python3 -m bot.index_qurish
    if vektorlar_soni() == 0:
        print("Vektor baza bo'sh — indekslanmoqda...", flush=True)
        bazani_yuklash()
    print("Bot ishga tushdi, polling boshlandi.", flush=True)
    asyncio.run(dp.start_polling(bot))
