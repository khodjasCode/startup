"""Chat: /api/savol — bot/rag.py yadrosini HTTP orqali ochib beradi.

RAG yadrosi (chromadb, Gemini kaliti, indekslangan baza) o'rnatilmagan bo'lsa
ham sayt ishlashi kerak: katalog, savol-javob, manbalar va avtorizatsiya
bularsiz ham to'liq ishlaydi. Shuning uchun `bot.rag` faqat birinchi savol
kelganda import qilinadi va import qilib bo'lmasa — tushunarli xabar qaytadi.
"""

import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api", tags=["chat"])

logger = logging.getLogger(__name__)

TILLAR = ("uz", "ru", "en")

# RAG yadrosi yo'q bo'lgan holat uchun xabar (kutilmagan xatolik emas — sozlash kerak).
YADRO_YOQ_XABARI = {
    "uz": (
        "⚙️ Chat hozircha sozlanmagan: qidiruv yadrosi ishga tushirilmagan.\n\n"
        "Sayt bo'limlari (kategoriyalar, xizmatlar, savol-javob) to'liq ishlaydi — "
        "kerakli xizmatni katalogdan topishingiz mumkin."
    ),
    "ru": (
        "⚙️ Чат пока не настроен: поисковое ядро не запущено.\n\n"
        "Разделы сайта (категории, услуги, вопрос-ответ) работают полностью — "
        "нужную услугу можно найти в каталоге."
    ),
    "en": (
        "⚙️ Chat is not configured yet: the search core is not running.\n\n"
        "The rest of the site (categories, services, Q&A) works fully — "
        "you can find the service you need in the catalog."
    ),
}

# Har bir brauzer sessiyasi uchun suhbat tarixi (aniqlashtiruvchi savol-javob
# oqimi uchun). MVP uchun xotirada saqlanadi; server qayta tushsa yo'qoladi.
SUHBATLAR: dict[str, list[dict]] = {}
TARIX_UZUNLIGI = 8  # so'nggi N ta xabar (fuqaro+bot) saqlanadi

_yadro: Any | None = None
_yadro_tekshirildi = False


def _rag_yadrosi() -> Any | None:
    """bot.rag ni bir marta import qilishga urinadi; bo'lmasa None qaytaradi."""
    global _yadro, _yadro_tekshirildi
    if not _yadro_tekshirildi:
        _yadro_tekshirildi = True
        try:
            from bot import rag

            _yadro = rag
        except Exception as xato:  # ImportError, SystemExit (kalit yo'q) va h.k.
            logger.warning("RAG yadrosi mavjud emas, chat o'chirilgan holatda: %s", xato)
            _yadro = None
    return _yadro


class SavolSorovi(BaseModel):
    savol: str = Field(max_length=2000)
    session_id: str = Field(default="default", max_length=100)
    til: str = "uz"


class JavobNatijasi(BaseModel):
    javob: str


@router.post("/savol", response_model=JavobNatijasi)
async def savol_sorash(sorov: SavolSorovi) -> JavobNatijasi:
    if not sorov.savol.strip():
        return JavobNatijasi(javob="Iltimos, savolingizni matn ko'rinishida yozing.")

    til = sorov.til if sorov.til in TILLAR else "uz"

    yadro = _rag_yadrosi()
    if yadro is None:
        return JavobNatijasi(javob=YADRO_YOQ_XABARI[til])

    tarix = SUHBATLAR.setdefault(sorov.session_id, [])
    tarix.append({"rol": "fuqaro", "matn": sorov.savol})

    try:
        javob = yadro.javob_olish(tarix, til)
        tarix.append({"rol": "bot", "matn": javob})
        del tarix[:-TARIX_UZUNLIGI]
    except yadro.TokenlarTugadi:
        javob = yadro.TOKENLAR_TUGADI_XABARI_TARJIMALARI[til]
        tarix.pop()  # foydalanuvchi savoli javobsiz qoldi, tarixga qo'shilmasin
    except Exception:
        logger.exception("Javob olishda kutilmagan xatolik")
        javob = yadro.XATOLIK_XABARI_TARJIMALARI[til]
        tarix.pop()

    return JavobNatijasi(javob=javob)


@router.post("/suhbatni-tozalash")
async def suhbatni_tozalash(sorov: dict) -> dict:
    """Chat sarlavhasidagi "tozalash" tugmasi uchun: server tarixini o'chiradi."""
    SUHBATLAR.pop(str(sorov.get("session_id", "")), None)
    return {"holat": "ok"}
