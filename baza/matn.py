"""Manba fayllaridagi turli shakldagi qiymatlarni matnga keltirish yordamchilari.

`data/*.json` da bir xil maydon ba'zan satr, ba'zan ro'yxat yoki lug'at bo'lib
keladi (turli portallardan yig'ilgan). Shu yerdagi funksiyalar ularni yagona
ko'rinishga keltiradi — baza to'ldirishda ham, javob yasashda ham ishlatiladi.
"""

from __future__ import annotations


def matn(qiymat) -> str:
    """Qiymat lug'at yoki ro'yxat bo'lsa ham o'qiladigan matnga aylantiradi."""
    if not qiymat:
        return ""
    if isinstance(qiymat, str):
        return qiymat.strip()
    if isinstance(qiymat, list):
        return "; ".join(matn(x) for x in qiymat if x)
    if isinstance(qiymat, dict):
        return "; ".join(f"{k}: {matn(v)}" for k, v in qiymat.items() if v)
    return str(qiymat)


def royxat(qiymat) -> list[str]:
    if not qiymat:
        return []
    if isinstance(qiymat, list):
        return [matn(x) for x in qiymat if x]
    return [matn(qiymat)]


def qirqish(xom: str, uzunlik: int) -> str:
    xom = (xom or "").strip()
    if len(xom) <= uzunlik:
        return xom
    return xom[:uzunlik].rsplit(" ", 1)[0] + "…"
