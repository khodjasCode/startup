"""Katalog: sohalar, xizmatlar, manbalar, savol-javob — Postgres'dan.

Yozuvlar `xizmatlar` va `manbalar` jadvallarida turadi (ular `data/*.json` dan
`python3 -m baza.kochirish` orqali to'ldiriladi). Baza bir marta o'qilib
xotirada keshlanadi (`web.xizmat.kesh`), filtrlash va guruhlash esa shu
ro'yxat ustida bajariladi — katalog kichik (~300 yozuv) va deyarli o'zgarmaydi,
shuning uchun har bir so'rov uchun bazaga borish keraksiz kechikish beradi.

RAG uchun ChromaDB ishlatiladi; saytdagi bo'limlar esa faqat shu jadvallardan
oziqlanadi.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import baza
from baza.matn import qirqish
from web.xizmat import tarjima_bazasi
from web.xizmat.kesh import Kesh

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
            "tavsif": qirqish(self.tavsif, 220),
            "url": self.url,
            "faq": self.faq,
            "kategoriya": self.kategoriya,
            # Rus/ingliz tarjimasi (bo'lsa) — frontend joriy tilga qarab tanlaydi.
            "i18n": tarjima_bazasi.xizmat_tarjimasi(self.id),
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
            "i18n": tarjima_bazasi.xizmat_tarjimasi(self.id),
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
            "i18n": tarjima_bazasi.manba_tarjimasi(self.kalit),
        }


XIZMAT_MAYDONLARI = (
    "id",
    "manba",
    "soha",
    "nomi",
    "tavsif",
    "url",
    "faq",
    "kategoriya",
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


def _xizmat(qator: dict) -> Xizmat:
    return Xizmat(**{maydon: qator[maydon] for maydon in XIZMAT_MAYDONLARI})


def _manba(qator: dict) -> Manba:
    return Manba(
        kalit=qator["kalit"],
        nomi=qator["nomi"],
        url=qator["url"],
        tavsif=qator["tavsif"],
        aloqa=qator["aloqa"],
        kirish_tartibi=qator["kirish_tartibi"],
        yigilgan_sana=qator["yigilgan_sana"],
        xizmatlar_soni=qator["xizmatlar_soni"],
    )


def _yuklash() -> tuple[list[Xizmat], list[Manba]]:
    """Butun katalogni bazadan o'qiydi (`tartib` — manba fayllaridagi asl ketma-ketlik)."""
    xizmatlar = [
        _xizmat(q)
        for q in baza.sorov(
            f"select {', '.join(XIZMAT_MAYDONLARI)} from xizmatlar order by tartib, id"
        )
    ]
    manbalar = [
        _manba(q) for q in baza.sorov("select * from manbalar order by tartib, kalit")
    ]
    return xizmatlar, manbalar


_kesh: Kesh[tuple[list[Xizmat], list[Manba]]] = Kesh(_yuklash)


def keshni_tozalash() -> None:
    """Baza yangilangach chaqiriladi — keyingi so'rov yangi ma'lumotni oladi."""
    _kesh.tozalash()
    tarjima_bazasi.keshni_tozalash()


def barcha_xizmatlar() -> list[Xizmat]:
    return _kesh.olish()[0]


def barcha_manbalar() -> list[Manba]:
    return _kesh.olish()[1]


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
                    "i18n": tarjima_bazasi.xizmat_tarjimasi(y.id),
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
