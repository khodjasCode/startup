"""Xizmatlar mazmunini ru/en tiliga tarjima qilingan qatlam.

`data/*.json` dagi asl matnlar faqat o'zbekcha (haqiqiy manba — my.gov.uz,
lex.uz va h.k. shu tilda yig'ilgan). Har bir yozuv uchun rus/ingliz tarjimasi
`data/i18n/*.json` fayllarida saqlanadi, kalit — xizmatning to'liq id'si
(`katalog_bazasi.Xizmat.id`), qiymat — `{"ru": {...}, "en": {...}}`.

Fayllar bir nechta bo'lakka bo'lingan bo'lishi mumkin (masalan
`my-gov.part1.json`, `my-gov.part2.json`) — hammasi shu papkadan o'qib,
kalitlar bo'yicha birlashtiriladi.
"""

from __future__ import annotations

import json
from functools import lru_cache

from web.config import DATA_YOLI

TARJIMA_PAPKASI = DATA_YOLI / "i18n"
MANBALAR_TARJIMASI_FAYLI = TARJIMA_PAPKASI / "manbalar.json"

# Tarjima qilinadigan maydonlar — Xizmat.qisqa()/toliq() bilan bir xil nomlar.
TARJIMA_MAYDONLARI = (
    "nomi",
    "tavsif",
    "muammolar",
    "qadamlar",
    "hujjatlar",
    "muddat",
    "narx",
    "aloqa",
    "kimlar_uchun",
    "idora",
    "qoshimcha",
)


@lru_cache(maxsize=1)
def _yuklash() -> dict[str, dict[str, dict]]:
    """`{xizmat_id: {"ru": {...}, "en": {...}}}` — barcha bo'lak fayllardan birlashtirilgan.

    `manbalar.json` bu yerga kirmaydi — u boshqa kalit fazosida (xizmat id
    emas, manba kaliti) va boshqa maydonlarga ega, shuning uchun alohida
    `_manbalar_yuklash()` orqali o'qiladi.
    """
    natija: dict[str, dict[str, dict]] = {}
    if not TARJIMA_PAPKASI.is_dir():
        return natija

    for fayl in sorted(TARJIMA_PAPKASI.glob("*.json")):
        if fayl == MANBALAR_TARJIMASI_FAYLI:
            continue
        try:
            xom = json.loads(fayl.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(xom, dict):
            natija.update(xom)

    return natija


@lru_cache(maxsize=1)
def _manbalar_yuklash() -> dict[str, dict[str, dict]]:
    """`{manba_kaliti: {"ru": {...}, "en": {...}}}`."""
    if not MANBALAR_TARJIMASI_FAYLI.is_file():
        return {}
    try:
        xom = json.loads(MANBALAR_TARJIMASI_FAYLI.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return xom if isinstance(xom, dict) else {}


def manba_tarjimasi(kalit: str) -> dict[str, dict] | None:
    """Berilgan manba (my-gov, lex, ...) uchun `{"ru": {...}, "en": {...}}`."""
    return _manbalar_yuklash().get(kalit)


def xizmat_tarjimasi(xizmat_id: str) -> dict[str, dict] | None:
    """Berilgan xizmat uchun `{"ru": {...}, "en": {...}}`, topilmasa None."""
    return _yuklash().get(xizmat_id)


def tarjimalar_soni() -> int:
    return len(_yuklash())
