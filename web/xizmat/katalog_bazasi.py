"""Bilim bazasi fayllarini (data/*.json) yagona ko'rinishga keltirib o'qish.

RAG uchun ChromaDB ishlatiladi, lekin saytdagi "Kategoriyalar", "Barcha bazalar",
"Manbalar" va "Savol-javob" bo'limlari to'g'ridan-to'g'ri shu JSON fayllardan
oziqlanadi — qo'shimcha baza ham, indekslash ham talab qilinmaydi.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from web.config import (
    BILIM_BAZASI_YOLI,
    LEX_YOLI,
    MY_GOV_YOLI,
    PM_GOV_YOLI,
    SAVOL_JAVOB_YOLI,
)

# Manba kaliti → (fayl yo'li, ko'rinadigan nom)
MANBA_FAYLLARI: dict[str, Path] = {
    "my-gov": MY_GOV_YOLI,
    "pm-gov": PM_GOV_YOLI,
    "lex": LEX_YOLI,
    "savol-javob": SAVOL_JAVOB_YOLI,
}

# Kategoriyasiz savol-javoblar shu guruhga tushadi.
FAQ_BOSHQA = "Boshqa savollar"


@dataclass(slots=True)
class Xizmat:
    """Bitta xizmat/yozuv — barcha manbalar uchun yagona shakl."""

    id: str
    manba: str
    soha: str
    nomi: str
    tavsif: str = ""
    url: str = ""
    # Yozuv "savol-javob" ko'rinishidami (xizmat emas, huquqiy savolga javob).
    faq: bool = False
    # Savol-javoblar uchun mavzu guruhi ("Oilaviy munosabatlar" va h.k.).
    kategoriya: str = ""
    muammolar: list[str] = field(default_factory=list)
    qadamlar: list[str] = field(default_factory=list)
    hujjatlar: list[str] = field(default_factory=list)
    muddat: str = ""
    narx: str = ""
    aloqa: str = ""
    kimlar_uchun: str = ""
    idora: str = ""
    qoshimcha: str = ""

    def qisqa(self) -> dict:
        """Ro'yxatlar uchun yengil ko'rinish (butun matnlarsiz)."""
        return {
            "id": self.id,
            "manba": self.manba,
            "soha": self.soha,
            "nomi": self.nomi,
            "tavsif": _qirqish(self.tavsif, 220),
            "url": self.url,
            "faq": self.faq,
            "kategoriya": self.kategoriya,
        }

    def toliq(self) -> dict:
        return {
            "id": self.id,
            "manba": self.manba,
            "soha": self.soha,
            "nomi": self.nomi,
            "tavsif": self.tavsif,
            "url": self.url,
            "muammolar": self.muammolar,
            "qadamlar": self.qadamlar,
            "hujjatlar": self.hujjatlar,
            "muddat": self.muddat,
            "narx": self.narx,
            "aloqa": self.aloqa,
            "kimlar_uchun": self.kimlar_uchun,
            "idora": self.idora,
            "qoshimcha": self.qoshimcha,
            "faq": self.faq,
            "kategoriya": self.kategoriya,
        }


@dataclass(slots=True)
class Manba:
    """Portal (my.gov.uz, lex.uz, ...) haqida ma'lumot."""

    kalit: str
    nomi: str
    url: str
    tavsif: str
    aloqa: str
    kirish_tartibi: list[str]
    yigilgan_sana: str
    xizmatlar_soni: int

    def dict(self) -> dict:
        return {
            "kalit": self.kalit,
            "nomi": self.nomi,
            "url": self.url,
            "tavsif": self.tavsif,
            "aloqa": self.aloqa,
            "kirish_tartibi": self.kirish_tartibi,
            "yigilgan_sana": self.yigilgan_sana,
            "xizmatlar_soni": self.xizmatlar_soni,
        }


def _qirqish(matn: str, uzunlik: int) -> str:
    matn = (matn or "").strip()
    if len(matn) <= uzunlik:
        return matn
    return matn[:uzunlik].rsplit(" ", 1)[0] + "…"


def _matn(qiymat) -> str:
    """Qiymat lug'at yoki ro'yxat bo'lsa ham o'qiladigan matnga aylantiradi."""
    if not qiymat:
        return ""
    if isinstance(qiymat, str):
        return qiymat.strip()
    if isinstance(qiymat, list):
        return "; ".join(_matn(x) for x in qiymat if x)
    if isinstance(qiymat, dict):
        return "; ".join(f"{k}: {_matn(v)}" for k, v in qiymat.items() if v)
    return str(qiymat)


def _royxat(qiymat) -> list[str]:
    if not qiymat:
        return []
    if isinstance(qiymat, list):
        return [_matn(x) for x in qiymat if x]
    return [_matn(qiymat)]


def _json_oqish(yol: Path) -> dict:
    if not yol.is_file():
        return {}
    return json.loads(yol.read_text(encoding="utf-8"))


def _portal_yozuvi(kalit: str, yozuv: dict) -> Xizmat:
    """Bitta yozuv. Fayllarda ikki xil shakl uchraydi:

    · xizmat: `xizmat_nomi` + `tavsif` + `qadamlar` (my.gov.uz, pm.gov.uz, lex xizmatlari)
    · savol-javob: `savol` + `qisqa_javob` + `huquqiy_asos` (advice.uz, lex huquqiy javoblari)
    """
    savol = _matn(yozuv.get("savol"))
    faq = bool(savol)

    qoshimcha = [_matn(yozuv.get("qoshimcha"))]
    if yozuv.get("huquqiy_asos"):
        qoshimcha.append(_matn(yozuv.get("huquqiy_asos")))

    return Xizmat(
        id=f"{kalit}.{yozuv.get('id', '')}",
        manba=kalit,
        soha=_matn(yozuv.get("soha")) or "Boshqa",
        nomi=savol or _matn(yozuv.get("xizmat_nomi")),
        tavsif=_matn(yozuv.get("qisqa_javob")) or _matn(yozuv.get("tavsif")),
        url=_matn(yozuv.get("url")),
        faq=faq,
        kategoriya=_matn(yozuv.get("kategoriya")),
        muammolar=_royxat(yozuv.get("muammolar")),
        qadamlar=_royxat(yozuv.get("qadamlar")),
        hujjatlar=_royxat(yozuv.get("kerakli_hujjatlar")),
        muddat=_matn(yozuv.get("muddat")),
        narx=_matn(yozuv.get("narx")),
        aloqa=_matn(yozuv.get("aloqa")),
        kimlar_uchun=_matn(yozuv.get("kimlar_uchun")),
        idora=_matn(yozuv.get("korsatuvchi_idora")),
        qoshimcha=" · ".join(q for q in qoshimcha if q),
    )


def _portal_xizmatlarini_oqish(kalit: str, xom: dict) -> list[Xizmat]:
    return [
        _portal_yozuvi(kalit, yozuv) for yozuv in xom.get("xizmatlar", []) if yozuv.get("id")
    ]


def _bilim_bazasini_oqish() -> list[Xizmat]:
    """bilim_bazasi.json boshqa sxemada — uni ham yagona shaklga keltiramiz."""
    xom = _json_oqish(BILIM_BAZASI_YOLI)
    xizmatlar = []
    for yozuv in xom.get("yozuvlar", []):
        if not yozuv.get("id"):
            continue
        idora = yozuv.get("masul_idora") or {}
        xizmatlar.append(
            Xizmat(
                id=f"bilim-bazasi.{yozuv['id']}",
                manba="bilim-bazasi",
                soha=_matn(yozuv.get("kategoriya")) or "Boshqa",
                nomi=_qirqish(_matn(yozuv.get("muammo")), 110),
                tavsif=_matn(yozuv.get("muammo")),
                url="",
                muammolar=_royxat(yozuv.get("kalit_sozlar")),
                qadamlar=_royxat(yozuv.get("murojaat_tartibi")),
                hujjatlar=_royxat(yozuv.get("kerakli_hujjatlar")),
                muddat=_matn(yozuv.get("korish_muddati")),
                aloqa=_matn(yozuv.get("murojaat_kanallari")),
                idora=_matn(idora.get("nomi")),
                qoshimcha=_matn(yozuv.get("eskalatsiya")),
            )
        )
    return xizmatlar


@lru_cache(maxsize=1)
def _yuklash() -> tuple[list[Xizmat], list[Manba]]:
    xizmatlar: list[Xizmat] = []
    manbalar: list[Manba] = []

    for kalit, yol in MANBA_FAYLLARI.items():
        xom = _json_oqish(yol)
        if not xom:
            continue
        portal_xizmatlari = _portal_xizmatlarini_oqish(kalit, xom)
        xizmatlar.extend(portal_xizmatlari)

        portal = xom.get("portal") or {}
        manbalar.append(
            Manba(
                kalit=kalit,
                nomi=_matn(portal.get("nomi")) or kalit,
                url=_matn(portal.get("url")),
                tavsif=_matn(portal.get("tavsif")),
                aloqa=_matn(
                    portal.get("aloqa_markazi") or portal.get("aloqa") or portal.get("qidiruv")
                ),
                kirish_tartibi=_royxat(portal.get("kirish_tartibi")),
                yigilgan_sana=_matn(xom.get("yigilgan_sana")),
                xizmatlar_soni=len(portal_xizmatlari),
            )
        )

    bilim = _bilim_bazasini_oqish()
    if bilim:
        xizmatlar.extend(bilim)
        manbalar.append(
            Manba(
                kalit="bilim-bazasi",
                nomi="Compass bilim bazasi (qo'lda tayyorlangan yozuvlar)",
                url="",
                tavsif=(
                    "Eng ko'p uchraydigan muammolar bo'yicha qo'lda yozilgan yo'riqnomalar: "
                    "qaysi idora, qanday hujjat, qanday tartib."
                ),
                aloqa="",
                kirish_tartibi=[],
                yigilgan_sana="",
                xizmatlar_soni=len(bilim),
            )
        )

    return xizmatlar, manbalar


def barcha_xizmatlar() -> list[Xizmat]:
    return _yuklash()[0]


def barcha_manbalar() -> list[Manba]:
    return _yuklash()[1]


def xizmat_topish(xizmat_id: str) -> Xizmat | None:
    return next((x for x in barcha_xizmatlar() if x.id == xizmat_id), None)


def xizmatlar_royxati() -> list[Xizmat]:
    """Faqat xizmatlar (savol-javoblarsiz)."""
    return [x for x in barcha_xizmatlar() if not x.faq]


def faq_royxati() -> list[Xizmat]:
    """Faqat savol-javoblar."""
    return [x for x in barcha_xizmatlar() if x.faq]


def sohalar() -> list[dict]:
    """Xizmat sohalari ro'yxati, yozuvlar soni bilan."""
    hisob: dict[str, int] = {}
    for xizmat in xizmatlar_royxati():
        hisob[xizmat.soha] = hisob.get(xizmat.soha, 0) + 1
    return [
        {"nomi": nomi, "soni": soni}
        for nomi, soni in sorted(hisob.items(), key=lambda p: (-p[1], p[0]))
    ]


def faq_guruhlari(matn: str = "") -> list[dict]:
    """Savol-javoblar mavzular bo'yicha guruhlangan holda (my.gov.uz/faq uslubi).

    `kategoriya` ko'rsatilmagan yozuvlar manbasiga qarab umumiy guruhga tushadi.
    """
    guruhlar: dict[str, list[Xizmat]] = {}
    for yozuv in qidirish(faq_royxati(), matn=matn):
        nomi = yozuv.kategoriya or (yozuv.soha if yozuv.manba != "savol-javob" else FAQ_BOSHQA)
        guruhlar.setdefault(nomi, []).append(yozuv)

    return [
        {
            "nomi": nomi,
            "soni": len(yozuvlar),
            "savollar": [
                {
                    "id": y.id,
                    "savol": y.nomi,
                    "javob": y.tavsif,
                    "izoh": y.qoshimcha,
                    "url": y.url,
                }
                for y in yozuvlar
            ],
        }
        # Kategoriyali guruhlar oldinda, "Boshqa savollar" doim oxirida.
        for nomi, yozuvlar in sorted(
            guruhlar.items(), key=lambda p: (p[0] == FAQ_BOSHQA, -len(p[1]), p[0])
        )
    ]


def qidirish(
    xizmatlar: list[Xizmat] | None = None,
    *,
    soha: str = "",
    matn: str = "",
) -> list[Xizmat]:
    """Soha va erkin matn bo'yicha oddiy filtr (RAG emas — aniq matn qidiruvi)."""
    natija = xizmatlar if xizmatlar is not None else barcha_xizmatlar()

    if soha:
        natija = [x for x in natija if x.soha == soha]

    kalit = matn.strip().lower()
    if kalit:
        natija = [
            x
            for x in natija
            if kalit in x.nomi.lower()
            or kalit in x.tavsif.lower()
            or any(kalit in m.lower() for m in x.muammolar)
        ]

    return natija


def statistika() -> dict:
    return {
        "jami_yozuvlar": len(barcha_xizmatlar()),
        "sohalar_soni": len(sohalar()),
        "faq_soni": len(faq_royxati()),
        "manbalar": [m.dict() for m in barcha_manbalar()],
    }
