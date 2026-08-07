"""Avtorizatsiya: telefon raqami → SMS kod → sessiya.

Sessiya tokeni httpOnly cookie'da yuriladi — JavaScript uni o'qiy olmaydi,
shuning uchun XSS holatida ham token o'g'irlanmaydi.

⚠️ SMS hozircha yuborilmaydi (mock): kod javobda qaytariladi va interfeysda
ko'rsatiladi. Provayder ulangach `mock_kod` maydonini olib tashlash kifoya.

Hisoblar, sessiyalar va kodlar Postgres'da saqlanadi. Marshrutlar `async def`
emas: baza chaqiruvi bloklovchi, FastAPI ularni alohida oqimda bajaradi.
"""

from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import BaseModel, Field

from web.config import COOKIE_SAMESITE, COOKIE_SECURE
from web.xizmat import foydalanuvchilar_bazasi as baza

router = APIRouter(prefix="/api/auth", tags=["auth"])

COOKIE_NOMI = "compass_sessiya"
COOKIE_UMRI = baza.SESSIYA_KUNI * 24 * 60 * 60


class SmsSorovi(BaseModel):
    telefon: str = Field(max_length=25)
    tugilgan_sana: str = Field(max_length=20)


class TasdiqSorovi(BaseModel):
    telefon: str = Field(max_length=25)
    kod: str = Field(max_length=10)
    hudud: str = Field(default="", max_length=40)


@router.post("/sms")
def sms_yuborish(sorov: SmsSorovi) -> dict:
    try:
        kod, muddat = baza.sms_yuborish(sorov.telefon, sorov.tugilgan_sana)
    except baza.KirishXatosi as xato:
        raise HTTPException(status_code=400, detail=str(xato)) from xato
    return {
        "yuborildi": True,
        "muddat_soniya": muddat,
        "qayta_yuborish_soniya": baza.KOD_QAYTA_YUBORISH_SONIYA,
        "mock_kod": kod,  # ⚠️ faqat mock rejimida
    }


@router.post("/tasdiqlash")
def tasdiqlash(sorov: TasdiqSorovi, javob: Response) -> dict:
    try:
        foydalanuvchi, token = baza.tasdiqlash(sorov.telefon, sorov.kod, sorov.hudud)
    except baza.KirishXatosi as xato:
        raise HTTPException(status_code=400, detail=str(xato)) from xato

    javob.set_cookie(
        COOKIE_NOMI,
        token,
        max_age=COOKIE_UMRI,
        httponly=True,
        # Frontend alohida domenda bo'lsa "none" + secure kerak (web/config.py).
        samesite=COOKIE_SAMESITE,
        secure=COOKIE_SECURE,
        path="/",
    )
    return {"foydalanuvchi": foydalanuvchi.dict()}


@router.post("/chiqish")
def chiqish(javob: Response, compass_sessiya: str | None = Cookie(default=None)) -> dict:
    baza.chiqish(compass_sessiya)
    # O'chirish uchun cookie'ning barcha belgilari o'rnatilgandagi bilan bir xil bo'lishi kerak.
    javob.delete_cookie(
        COOKIE_NOMI, path="/", httponly=True, samesite=COOKIE_SAMESITE, secure=COOKIE_SECURE
    )
    return {"holat": "ok"}


@router.get("/men")
def men(compass_sessiya: str | None = Cookie(default=None)) -> dict:
    foydalanuvchi = baza.sessiya_boyicha(compass_sessiya)
    return {"foydalanuvchi": foydalanuvchi.dict() if foydalanuvchi else None}
