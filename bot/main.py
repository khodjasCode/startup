# Telegram qismi (aiogram 3, long polling)
# Ishga tushirish:  python -m bot.main

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from bot.config import BOT_TOKEN
from bot.rag import javob_olish
from bot.index_qurish import bazani_yuklash

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


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
    try:
        javob = javob_olish(msg.text)
    except Exception as e:
        javob = "Kechirasiz, texnik xatolik. Birozdan keyin qayta urinib ko'ring."
        print("XATO:", e)
    await msg.answer(javob)


if __name__ == "__main__":
    bazani_yuklash()
    asyncio.run(dp.start_polling(bot))
