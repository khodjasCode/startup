"""Katalog: sohalar, xizmatlar, manbalar, savol-javob va statistika.

Ma'lumot Postgres'dan olinadi (`web.xizmat.katalog_bazasi` uni keshlab turadi).
Marshrutlar `async def` emas — baza chaqiruvi bloklovchi, shuning uchun FastAPI
ularni alohida oqimda bajarishi kerak.
"""

from fastapi import APIRouter, HTTPException, Query

from web.xizmat import katalog_bazasi as baza

router = APIRouter(prefix="/api", tags=["katalog"])


@router.get("/sohalar")
def sohalar() -> dict:
    return {"sohalar": baza.sohalar()}


@router.get("/xizmatlar")
def xizmatlar(
    soha: str = "",
    q: str = "",
    limit: int = Query(default=24, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict:
    """Xizmatlar ro'yxati: soha va matn bo'yicha filtr + sahifalash."""
    topildi = baza.qidirish(baza.xizmatlar_royxati(), soha=soha, matn=q)
    return {
        "jami": len(topildi),
        "xizmatlar": [x.qisqa() for x in topildi[offset : offset + limit]],
    }


@router.get("/xizmatlar/{xizmat_id}")
def xizmat(xizmat_id: str) -> dict:
    topildi = baza.xizmat_topish(xizmat_id)
    if topildi is None:
        raise HTTPException(status_code=404, detail="Xizmat topilmadi")
    return topildi.toliq()


@router.get("/manbalar")
def manbalar() -> dict:
    return {"manbalar": [m.dict() for m in baza.barcha_manbalar()]}


@router.get("/savol-javob")
def savol_javob(q: str = "") -> dict:
    """Ko'p so'raladigan savollar — mavzular bo'yicha guruhlangan."""
    guruhlar = baza.faq_guruhlari(q)
    return {"jami": sum(g["soni"] for g in guruhlar), "guruhlar": guruhlar}


@router.get("/statistika")
def statistika() -> dict:
    return baza.statistika()
