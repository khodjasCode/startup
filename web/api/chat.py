"""Chat: /api/savol — bot/rag.py yadrosini HTTP orqali ochib beradi.

RAG yadrosi (Gemini kaliti, indekslangan vektor bazasi) sozlanmagan bo'lsa
ham sayt ishlashi kerak: katalog, savol-javob, manbalar va avtorizatsiya
bularsiz ham to'liq ishlaydi. Shuning uchun `bot.rag` faqat birinchi savol
kelganda import qilinadi va import qilib bo'lmasa — tushunarli xabar qaytadi.

Marshrutlar `async def` emas: ular ichida bloklovchi chaqiruvlar bor (Postgres
va Gemini) — FastAPI oddiy `def` marshrutini alohida oqimda bajaradi, shuning
uchun hodisa halqasi (soat WebSocket'i va boshqa so'rovlar) to'xtab qolmaydi.
"""

import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from baza import suhbat

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
        # `bot.config` kalit topilmasa SystemExit ko'taradi — u Exception emas,
        # shuning uchun alohida sanab o'tiladi (aks holda so'rov 500 bilan tugaydi).
        except (Exception, SystemExit) as xato:
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
def savol_sorash(sorov: SavolSorovi) -> JavobNatijasi:
    if not sorov.savol.strip():
        return JavobNatijasi(javob="Iltimos, savolingizni matn ko'rinishida yozing.")

    til = sorov.til if sorov.til in TILLAR else "uz"

    yadro = _rag_yadrosi()
    if yadro is None:
        return JavobNatijasi(javob=YADRO_YOQ_XABARI[til])

    # Bazadagi tarix + shu savol: yadroga to'liq oqim beriladi, lekin bazaga
    # savol javob bilan birga (muvaffaqiyatli bo'lsagina) yoziladi.
    tarix = suhbat.tarix(sorov.session_id)
    tarix.append({"rol": "fuqaro", "matn": sorov.savol})

    try:
        javob = yadro.javob_olish(tarix, til)
        suhbat.saqlash(sorov.session_id, sorov.savol, javob, til)
    except yadro.TokenlarTugadi:
        javob = yadro.TOKENLAR_TUGADI_XABARI_TARJIMALARI[til]
    except Exception:
        logger.exception("Javob olishda kutilmagan xatolik")
        javob = yadro.XATOLIK_XABARI_TARJIMALARI[til]

    return JavobNatijasi(javob=javob)


@router.post("/suhbatni-tozalash")
def suhbatni_tozalash(sorov: dict) -> dict:
    """Chat sarlavhasidagi "tozalash" tugmasi uchun: server tarixini o'chiradi."""
    suhbat.tozalash(str(sorov.get("session_id", "")))
    return {"holat": "ok"}
