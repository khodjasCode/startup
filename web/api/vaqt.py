"""Toshkent vaqti: WebSocket orqali har soniyada yuboriladi.

Nega socket: brauzerdagi soat foydalanuvchi kompyuteridagi vaqtga bog'liq
(u noto'g'ri qo'yilgan bo'lishi mumkin). Server har soniyada aniq vaqtni
yuborib turadi, frontend esa xabarlar orasida o'zi tiklaydi.
"""

import asyncio
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from web.config import VAQT_MINTAQASI

router = APIRouter(tags=["vaqt"])

# O'zbekiston doimiy UTC+5 (yozgi vaqt yo'q), shuning uchun IANA bazasi
# (zoneinfo/tzdata) shart emas — u Windows'da odatda o'rnatilmagan bo'ladi.
_MINTAQA = timezone(timedelta(hours=5), VAQT_MINTAQASI)


def _hozir() -> dict:
    hozir = datetime.now(_MINTAQA)
    return {
        "iso": hozir.isoformat(timespec="seconds"),
        "mintaqa": VAQT_MINTAQASI,
        # Millisekundlar: frontend keyingi soniyaga aniq tekislanishi uchun.
        "ms": hozir.microsecond // 1000,
    }


@router.get("/api/vaqt")
async def vaqt() -> dict:
    """WebSocket ishlamagan holat uchun oddiy HTTP javob."""
    return _hozir()


@router.websocket("/ws/vaqt")
async def vaqt_socket(socket: WebSocket) -> None:
    await socket.accept()
    try:
        while True:
            await socket.send_json(_hozir())
            # Keyingi soniyaning boshiga tekislanib uxlaymiz.
            hozir = datetime.now(_MINTAQA)
            await asyncio.sleep(1 - hozir.microsecond / 1_000_000)
    except WebSocketDisconnect:
        return
    except (RuntimeError, ConnectionError):
        # Mijoz to'satdan uzilib qolgan — bu xato emas.
        return
