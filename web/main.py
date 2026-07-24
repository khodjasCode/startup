# Web interfeys: bot/rag.py dagi javob_olish() ni HTTP orqali ochib beradi.
# Ishga tushirish (repo root'dan):  uvicorn web.main:app --reload

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from bot.rag import javob_olish, TokenlarTugadi, TOKENLAR_TUGADI_XABARI

STATIC_YOLI = Path(__file__).parent / "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_YOLI), name="static")

# Har bir brauzer sessiyasi uchun suhbat tarixi (aniqlashtiruvchi savol-javob
# oqimi uchun). MVP uchun xotirada saqlanadi; server qayta tushsa yo'qoladi.
SUHBATLAR: dict[str, list[dict]] = {}
TARIX_UZUNLIGI = 8  # so'nggi N ta xabar (fuqaro+bot) saqlanadi


class SavolSorovi(BaseModel):
    savol: str
    session_id: str = "default"


class JavobNatijasi(BaseModel):
    javob: str


@app.get("/")
async def index():
    return FileResponse(STATIC_YOLI / "homepage.html")


@app.post("/api/savol", response_model=JavobNatijasi)
async def savol_sorash(sorov: SavolSorovi):
    if not sorov.savol.strip():
        return JavobNatijasi(javob="Iltimos, savolingizni matn ko'rinishida yozing.")

    tarix = SUHBATLAR.setdefault(sorov.session_id, [])
    tarix.append({"rol": "fuqaro", "matn": sorov.savol})

    try:
        javob = javob_olish(tarix)
        tarix.append({"rol": "bot", "matn": javob})
        del tarix[:-TARIX_UZUNLIGI]
    except TokenlarTugadi:
        javob = TOKENLAR_TUGADI_XABARI
        tarix.pop()  # foydalanuvchi savoli javobsiz qoldi, tarixga qo'shilmasin
    except Exception:
        javob = "Kechirasiz, texnik xatolik yuz berdi. Birozdan keyin qayta urinib ko'ring."

    return JavobNatijasi(javob=javob)
