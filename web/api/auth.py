"""Avtorizatsiya: telefon raqami → SMS kod → sessiya.

Sessiya tokeni httpOnly cookie'da yuriladi — JavaScript uni o'qiy olmaydi,
shuning uchun XSS holatida ham token o'g'irlanmaydi.

⚠️ SMS hozircha yuborilmaydi (mock): kod javobda qaytariladi va interfeysda
ko'rsatiladi. Provayder ulangach `mock_kod` maydonini olib tashlash kifoya.
"""

from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import BaseModel, Field

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
async def sms_yuborish(sorov: SmsSorovi) -> dict:
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
async def tasdiqlash(sorov: TasdiqSorovi, javob: Response) -> dict:
    try:
        foydalanuvchi, token = baza.tasdiqlash(sorov.telefon, sorov.kod, sorov.hudud)
    except baza.KirishXatosi as xato:
        raise HTTPException(status_code=400, detail=str(xato)) from xato

    javob.set_cookie(
        COOKIE_NOMI,
        token,
        max_age=COOKIE_UMRI,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return {"foydalanuvchi": foydalanuvchi.dict()}


@router.post("/chiqish")
async def chiqish(javob: Response, compass_sessiya: str | None = Cookie(default=None)) -> dict:
    baza.chiqish(compass_sessiya)
    javob.delete_cookie(COOKIE_NOMI, path="/")
    return {"holat": "ok"}


@router.get("/men")
async def men(compass_sessiya: str | None = Cookie(default=None)) -> dict:
    foydalanuvchi = baza.sessiya_boyicha(compass_sessiya)
    return {"foydalanuvchi": foydalanuvchi.dict() if foydalanuvchi else None}
