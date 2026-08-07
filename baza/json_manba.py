"""`data/*.json` fayllarini o'qib, bazaga yoziladigan qatorlarga aylantirish.

Bu yagona joy — undan keyin sayt ham, bot ham faqat Postgres bilan ishlaydi.
JSON fayllar manba (source of truth) bo'lib qoladi: ular yangilangach
`python3 -m baza.kochirish` qayta yuklaydi.
"""

from __future__ import annotations

import json
from pathlib import Path

from baza.matn import matn as _matn
from baza.matn import qirqish, royxat
from baza.muhit import LOYIHA_ILDIZI

DATA_YOLI = LOYIHA_ILDIZI / "data"
TARJIMA_PAPKASI = DATA_YOLI / "i18n"
MANBALAR_TARJIMASI_FAYLI = TARJIMA_PAPKASI / "manbalar.json"

BILIM_BAZASI_YOLI = DATA_YOLI / "bilim_bazasi.json"

# Manba kaliti → fayl yo'li. Tartib muhim: saytda shu ketma-ketlikda ko'rinadi.
MANBA_FAYLLARI: dict[str, Path] = {
    "my-gov": DATA_YOLI / "my-gov.json",
    "pm-gov": DATA_YOLI / "pm-gov.json",
    "lex": DATA_YOLI / "lex.json",
    "savol-javob": DATA_YOLI / "savol-javob.json",
}

BILIM_BAZASI_TAVSIFI = (
    "Eng ko'p uchraydigan muammolar bo'yicha qo'lda yozilgan yo'riqnomalar: "
    "qaysi idora, qanday hujjat, qanday tartib."
)


def _json_oqish(yol: Path) -> dict:
    if not yol.is_file():
        return {}
    return json.loads(yol.read_text(encoding="utf-8"))


def _portal_yozuvi(kalit: str, yozuv: dict) -> dict:
    """Bitta yozuv. Fayllarda ikki xil shakl uchraydi:

    · xizmat: `xizmat_nomi` + `tavsif` + `qadamlar` (my.gov.uz, pm.gov.uz, lex xizmatlari)
    · savol-javob: `savol` + `qisqa_javob` + `huquqiy_asos` (advice.uz, lex huquqiy javoblari)
    """
    savol = _matn(yozuv.get("savol"))

    qoshimcha = [_matn(yozuv.get("qoshimcha"))]
    if yozuv.get("huquqiy_asos"):
        qoshimcha.append(_matn(yozuv.get("huquqiy_asos")))

    return {
        "id": f"{kalit}.{yozuv.get('id', '')}",
        "manba": kalit,
        "soha": _matn(yozuv.get("soha")) or "Boshqa",
        "nomi": savol or _matn(yozuv.get("xizmat_nomi")),
        "tavsif": _matn(yozuv.get("qisqa_javob")) or _matn(yozuv.get("tavsif")),
        "url": _matn(yozuv.get("url")),
        "faq": bool(savol),
        "kategoriya": _matn(yozuv.get("kategoriya")),
        "muammolar": royxat(yozuv.get("muammolar")),
        "qadamlar": royxat(yozuv.get("qadamlar")),
        "hujjatlar": royxat(yozuv.get("kerakli_hujjatlar")),
        "muddat": _matn(yozuv.get("muddat")),
        "narx": _matn(yozuv.get("narx")),
        "aloqa": _matn(yozuv.get("aloqa")),
        "kimlar_uchun": _matn(yozuv.get("kimlar_uchun")),
        "idora": _matn(yozuv.get("korsatuvchi_idora")),
        "qoshimcha": " · ".join(q for q in qoshimcha if q),
    }


def _bilim_bazasi_yozuvi(yozuv: dict) -> dict:
    """bilim_bazasi.json boshqa sxemada — uni ham yagona shaklga keltiramiz."""
    idora = yozuv.get("masul_idora") or {}
    return {
        "id": f"bilim-bazasi.{yozuv['id']}",
        "manba": "bilim-bazasi",
        "soha": _matn(yozuv.get("kategoriya")) or "Boshqa",
        "nomi": qirqish(_matn(yozuv.get("muammo")), 110),
        "tavsif": _matn(yozuv.get("muammo")),
        "url": "",
        "faq": False,
        "kategoriya": "",
        "muammolar": royxat(yozuv.get("kalit_sozlar")),
        "qadamlar": royxat(yozuv.get("murojaat_tartibi")),
        "hujjatlar": royxat(yozuv.get("kerakli_hujjatlar")),
        "muddat": _matn(yozuv.get("korish_muddati")),
        "narx": "",
        "aloqa": _matn(yozuv.get("murojaat_kanallari")),
        "kimlar_uchun": "",
        "idora": _matn(idora.get("nomi")),
        "qoshimcha": _matn(yozuv.get("eskalatsiya")),
    }


def katalog() -> tuple[list[dict], list[dict]]:
    """`(xizmatlar, manbalar)` — bazaga yoziladigan qatorlar.

    Har bir yozuvga `tartib` qo'shiladi: fayllardagi asl ketma-ketlik saytda
    ham saqlanishi kerak (id bo'yicha saralash manbalarni aralashtirib yuboradi).
    """
    xizmatlar: list[dict] = []
    manbalar: list[dict] = []

    for kalit, yol in MANBA_FAYLLARI.items():
        xom = _json_oqish(yol)
        if not xom:
            continue

        portal_xizmatlari = [
            _portal_yozuvi(kalit, yozuv)
            for yozuv in xom.get("xizmatlar", [])
            if yozuv.get("id")
        ]
        xizmatlar.extend(portal_xizmatlari)

        portal = xom.get("portal") or {}
        manbalar.append(
            {
                "kalit": kalit,
                "nomi": _matn(portal.get("nomi")) or kalit,
                "url": _matn(portal.get("url")),
                "tavsif": _matn(portal.get("tavsif")),
                "aloqa": _matn(
                    portal.get("aloqa_markazi") or portal.get("aloqa") or portal.get("qidiruv")
                ),
                "kirish_tartibi": royxat(portal.get("kirish_tartibi")),
                "yigilgan_sana": _matn(xom.get("yigilgan_sana")),
                "xizmatlar_soni": len(portal_xizmatlari),
            }
        )

    bilim = [
        _bilim_bazasi_yozuvi(yozuv)
        for yozuv in _json_oqish(BILIM_BAZASI_YOLI).get("yozuvlar", [])
        if yozuv.get("id")
    ]
    if bilim:
        xizmatlar.extend(bilim)
        manbalar.append(
            {
                "kalit": "bilim-bazasi",
                "nomi": "Compass bilim bazasi (qo'lda tayyorlangan yozuvlar)",
                "url": "",
                "tavsif": BILIM_BAZASI_TAVSIFI,
                "aloqa": "",
                "kirish_tartibi": [],
                "yigilgan_sana": "",
                "xizmatlar_soni": len(bilim),
            }
        )

    for tartib, yozuv in enumerate(xizmatlar):
        yozuv["tartib"] = tartib
    for tartib, yozuv in enumerate(manbalar):
        yozuv["tartib"] = tartib

    return xizmatlar, manbalar


def tarjimalar() -> list[dict]:
    """`data/i18n/*.json` → `{tur, kalit, til, qiymat}` qatorlari.

    Fayllar bo'laklarga bo'lingan bo'lishi mumkin (`my-gov.part1.json` va h.k.),
    hammasi kalitlar bo'yicha birlashtiriladi. `manbalar.json` — alohida tur:
    uning kaliti xizmat id emas, manba kaliti.
    """
    if not TARJIMA_PAPKASI.is_dir():
        return []

    qatorlar: list[dict] = []
    for fayl in sorted(TARJIMA_PAPKASI.glob("*.json")):
        tur = "manba" if fayl == MANBALAR_TARJIMASI_FAYLI else "xizmat"
        try:
            xom = json.loads(fayl.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(xom, dict):
            continue
        for kalit, tillar in xom.items():
            if not isinstance(tillar, dict):
                continue
            for til, qiymat in tillar.items():
                if isinstance(qiymat, dict) and qiymat:
                    qatorlar.append(
                        {"tur": tur, "kalit": kalit, "til": til, "qiymat": qiymat}
                    )
    return qatorlar
