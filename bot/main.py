# Telegram qismi (aiogram 3, long polling)
# Ishga tushirish:  python -m bot.main

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from bot.config import BOT_TOKEN
from bot.rag import javob_olish, collection, TokenlarTugadi, TOKENLAR_TUGADI_XABARI
from bot.index_qurish import bazani_yuklash

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Har bir chat uchun suhbat tarixi (aniqlashtiruvchi savol-javob oqimi uchun).
# MVP uchun xotirada saqlanadi; bot qayta ishga tushsa tarix yo'qoladi.
SUHBAT_TARIXI: dict[int, list[dict]] = {}
TARIX_UZUNLIGI = 8  # so'nggi N ta xabar (fuqaro+bot) saqlanadi


@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "Assalomu alaykum! Men davlat xizmatlari bo'yicha yo'naltiruvchi botman.\n\n"
        "Muammoingizni oddiy tilda yozing (masalan: «3 kundan beri suv kelmayapti»), "
        "men qaysi idoraga qanday murojaat qilishni aytaman.\n\n"
        "⚠️ Men huquqiy maslahat bermayman — faqat yo'naltiraman."
    )


@dp.message()
async def savol(msg: types.Message):
    await msg.answer("Qidiryapman... ⏳")

    tarix = SUHBAT_TARIXI.setdefault(msg.chat.id, [])
    tarix.append({"rol": "fuqaro", "matn": msg.text})

    try:
        javob = javob_olish(tarix)
        tarix.append({"rol": "bot", "matn": javob})
        del tarix[:-TARIX_UZUNLIGI]
    except TokenlarTugadi:
        javob = TOKENLAR_TUGADI_XABARI
        tarix.pop()  # foydalanuvchi savoli javobsiz qoldi, tarixga qo'shilmasin
    except Exception as e:
        javob = "Kechirasiz, texnik xatolik. Birozdan keyin qayta urinib ko'ring."
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
