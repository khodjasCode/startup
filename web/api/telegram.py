"""Telegram webhook: POST /telegram/webhook.

Bepul hostingda doimiy ishlab turadigan alohida jarayon (long polling) yo'q,
shuning uchun serverda bot **webhook** orqali ishlaydi: Telegram yangilanishni
o'zi shu manzilga yuboradi va shu bilan uxlab qolgan servisni ham uyg'otadi.
Mahalliy ishlab chiqishda esa avvalgidek `python3 -m bot.main` (polling).

Xavfsizlik: Telegram har so'rovga `X-Telegram-Bot-Api-Secret-Token` sarlavhasini
qo'shadi (`setWebhook` da berilgan qiymat). Mos kelmasa — 403. Manzil ochiq
internetda turgani uchun bu tekshiruv majburiy, aks holda istalgan kishi
botga soxta yangilanish yubora olardi.

Webhook'ni ro'yxatdan o'tkazish: python3 -m web.telegram_webhook
"""

import logging
import os
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request

router = APIRouter(prefix="/telegram", tags=["telegram"])

logger = logging.getLogger(__name__)

SIR_SARLAVHASI = "x-telegram-bot-api-secret-token"


def sir() -> str:
    """`setWebhook` da berilgan maxfiy qiymat (bo'sh bo'lsa webhook o'chiq)."""
    return os.environ.get("TELEGRAM_WEBHOOK_SECRET", "").strip()


_bot: Any | None = None
_dp: Any | None = None
_tekshirildi = False


def _yadro() -> tuple[Any | None, Any | None]:
    """`bot.main` ni bir marta import qiladi (BOT_TOKEN/Gemini kaliti kerak).

    Kalitlar bo'lmasa sayt baribir ishlashi kerak, shuning uchun import
    xatosi yutiladi va webhook 503 qaytaradi — chat qismidagi bilan bir xil
    yondashuv (`web/api/chat.py`).
    """
    global _bot, _dp, _tekshirildi
    if not _tekshirildi:
        _tekshirildi = True
        try:
            from bot.main import bot, dp

            _bot, _dp = bot, dp
        except (Exception, SystemExit) as xato:
            logger.warning("Telegram boti sozlanmagan: %s", xato)
    return _bot, _dp


async def yopish() -> None:
    """Server to'xtaganda aiogram sessiyasini yopadi."""
    if _bot is not None:
        await _bot.session.close()


@router.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict:
    kutilgan = sir()
    if not kutilgan:
        raise HTTPException(status_code=503, detail="webhook_sozlanmagan")
    if x_telegram_bot_api_secret_token != kutilgan:
        raise HTTPException(status_code=403, detail="sir_notogri")

    bot, dp = _yadro()
    if bot is None or dp is None:
        raise HTTPException(status_code=503, detail="bot_sozlanmagan")

    from aiogram.types import Update

    yangilanish = Update.model_validate(await request.json(), context={"bot": bot})
    # Xatolik bo'lsa ham Telegram'ga 200 qaytaramiz: aks holda u shu
    # yangilanishni qayta-qayta yuboraveradi va navbat tiqilib qoladi.
    try:
        await dp.feed_webhook_update(bot, yangilanish)
    except Exception:
        logger.exception("Telegram yangilanishini qayta ishlashda xatolik")
    return {"holat": "ok"}
