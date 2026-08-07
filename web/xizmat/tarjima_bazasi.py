"""Xizmatlar mazmunini ru/en tiliga tarjima qilingan qatlam.

Manba matnlari faqat o'zbekcha (my.gov.uz, lex.uz va h.k. shu tilda yig'ilgan).
Tarjimalar Postgres'dagi `tarjimalar` jadvalida turadi: `tur` — 'xizmat' yoki
'manba', `kalit` — xizmat id'si (`katalog_bazasi.Xizmat.id`) yoki manba kaliti,
`til` — 'ru'/'en', `qiymat` — tarjima qilingan maydonlar (jsonb).

Jadval `data/i18n/*.json` fayllaridan to'ldiriladi: `python3 -m baza.kochirish`.
"""

from __future__ import annotations

import baza
from web.xizmat.kesh import Kesh

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


def _yuklash() -> dict[str, dict[str, dict[str, dict]]]:
    """`{tur: {kalit: {"ru": {...}, "en": {...}}}}` — butun jadval bir so'rovda.

    Tarjimalar ~700 qator, umumiy hajmi bir necha megabayt emas — ularni birdaniga
    o'qib xotirada saqlash har bir xizmat uchun alohida so'rov yuborishdan
    ancha tez (Xizmat.qisqa() har bir yozuv uchun tarjima so'raydi).
    """
    natija: dict[str, dict[str, dict[str, dict]]] = {"xizmat": {}, "manba": {}}
    for qator in baza.sorov("select tur, kalit, til, qiymat from tarjimalar"):
        natija.setdefault(qator["tur"], {}).setdefault(qator["kalit"], {})[qator["til"]] = qator[
            "qiymat"
        ]
    return natija


_kesh: Kesh[dict[str, dict[str, dict[str, dict]]]] = Kesh(_yuklash)


def keshni_tozalash() -> None:
    _kesh.tozalash()


def manba_tarjimasi(kalit: str) -> dict[str, dict] | None:
    """Berilgan manba (my-gov, lex, ...) uchun `{"ru": {...}, "en": {...}}`."""
    return _kesh.olish()["manba"].get(kalit)


def xizmat_tarjimasi(xizmat_id: str) -> dict[str, dict] | None:
    """Berilgan xizmat uchun `{"ru": {...}, "en": {...}}`, topilmasa None."""
    return _kesh.olish()["xizmat"].get(xizmat_id)


def tarjimalar_soni() -> int:
    """Tarjimasi bor xizmatlar soni."""
    return len(_kesh.olish()["xizmat"])
