import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.rag import javob_olish

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Salom! Men Yo'naltiruvchi botman.\n\n"
        "Muammoingizni oddiy tilda yozing — masalan: \"suv kelmayapti\".\n"
        "Men qaysi idoraga, qanday hujjatlar bilan murojaat qilish kerakligini aytib beraman."
    )


@dp.message()
async def savol_handler(message: Message):
    savol = message.text

    if not savol:
        await message.answer("Iltimos, savolingizni matn ko'rinishida yozing.")
        return

    kutish_xabari = await message.answer("Qidiryapman... ⏳")

    javob = javob_olish(savol)

    await kutish_xabari.edit_text(javob)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())