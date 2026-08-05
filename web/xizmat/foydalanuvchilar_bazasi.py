"""Telefon raqami bo'yicha kirish: raqam + tug'ilgan sana → SMS kod → sessiya.

Hozircha SMS **yuborilmaydi**: kod javobning o'zida qaytariladi va interfeysda
ko'rsatiladi (mock). Haqiqiy SMS-provayder ulangach, `sms_yuborish()` dagi
qaytariladigan kodni olib tashlash kifoya — qolgan mantiq o'zgarmaydi.

Ma'lumotlar JSON faylda saqlanadi (MVP). Yuklama ortsa haqiqiy bazaga
ko'chirilishi kerak.
"""

from __future__ import annotations

import json
import re
import secrets
import threading
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from web.config import FOYDALANUVCHILAR_YOLI as BAZA_YOLI

SESSIYA_KUNI = 30  # sessiya tokenining amal qilish muddati
KOD_MUDDATI_SONIYA = 300  # SMS kod 5 daqiqa amal qiladi
KOD_QAYTA_YUBORISH_SONIYA = 60  # shu vaqt o'tmasdan yangi kod so'ralmaydi
KOD_URINISHLARI = 5  # noto'g'ri kod kiritishga ruxsat etilgan urinishlar

# O'zbekiston raqami: 998 + 9 raqam.
TELEFON_SHABLONI = re.compile(r"^998\d{9}$")
ENG_KICHIK_YOSH = 14

_qulf = threading.Lock()


class KirishXatosi(Exception):
    """Kiritilgan ma'lumot noto'g'ri (xato kodi `args[0]` da)."""


@dataclass(slots=True)
class Foydalanuvchi:
    telefon: str
    tugilgan_sana: str
    yaratilgan: str
    # Foydalanuvchi tanlagan hudud (viloyat) identifikatori.
    hudud: str = ""

    def dict(self) -> dict:
        return {
            "telefon": self.telefon,
            "telefon_korinishi": telefon_korinishi(self.telefon),
            "tugilgan_sana": self.tugilgan_sana,
            "yaratilgan": self.yaratilgan,
            "hudud": self.hudud,
        }


def telefon_korinishi(telefon: str) -> str:
    """998901234567 → +998 90 123 45 67"""
    if not TELEFON_SHABLONI.match(telefon):
        return telefon
    t = telefon
    return f"+{t[:3]} {t[3:5]} {t[5:8]} {t[8:10]} {t[10:12]}"


def telefonni_tozalash(xom: str) -> str:
    """Foydalanuvchi kiritgan har qanday ko'rinishni 998XXXXXXXXX ga keltiradi."""
    raqamlar = re.sub(r"\D", "", xom or "")
    if len(raqamlar) == 9:  # 901234567
        raqamlar = "998" + raqamlar
    elif len(raqamlar) == 12 and raqamlar.startswith("998"):
        pass
    if not TELEFON_SHABLONI.match(raqamlar):
        raise KirishXatosi("telefon_notogri")
    return raqamlar


def sanani_tozalash(xom: str) -> str:
    """`dd.mm.yyyy` yoki `yyyy-mm-dd` → ISO (`yyyy-mm-dd`)."""
    xom = (xom or "").strip()
    for shakl in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            sana = datetime.strptime(xom, shakl).date()
            break
        except ValueError:
            continue
    else:
        raise KirishXatosi("sana_notogri")

    bugun = date.today()
    if sana > bugun or sana.year < 1900:
        raise KirishXatosi("sana_notogri")
    yosh = bugun.year - sana.year - ((bugun.month, bugun.day) < (sana.month, sana.day))
    if yosh < ENG_KICHIK_YOSH:
        raise KirishXatosi("yosh_kichik")
    return sana.isoformat()


def _hozir() -> datetime:
    return datetime.now(timezone.utc)


def _bazani_oqish() -> dict:
    if not BAZA_YOLI.is_file():
        return {"foydalanuvchilar": {}, "sessiyalar": {}, "kodlar": {}}
    try:
        xom = json.loads(BAZA_YOLI.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"foydalanuvchilar": {}, "sessiyalar": {}, "kodlar": {}}
    for kalit in ("foydalanuvchilar", "sessiyalar", "kodlar"):
        xom.setdefault(kalit, {})
    return xom


def _bazani_yozish(baza: dict) -> None:
    # Avval vaqtinchalik faylga yozib, so'ng o'rniga qo'yamiz — yozish yarim
    # yo'lda uzilib qolsa ham mavjud fayl buzilmaydi.
    vaqtinchalik = BAZA_YOLI.with_suffix(".json.tmp")
    vaqtinchalik.write_text(json.dumps(baza, ensure_ascii=False, indent=1), encoding="utf-8")
    vaqtinchalik.replace(BAZA_YOLI)


def _tozalash(baza: dict) -> None:
    """Muddati o'tgan sessiya va kodlarni olib tashlaydi."""
    hozir = _hozir()
    for token in [
        t
        for t, s in baza["sessiyalar"].items()
        if datetime.fromisoformat(s["muddat"]) < hozir
    ]:
        del baza["sessiyalar"][token]
    for telefon in [
        t
        for t, k in baza["kodlar"].items()
        if datetime.fromisoformat(k["muddat"]) < hozir
    ]:
        del baza["kodlar"][telefon]


def _foydalanuvchi(yozuv: dict) -> Foydalanuvchi:
    return Foydalanuvchi(
        telefon=yozuv["telefon"],
        tugilgan_sana=yozuv["tugilgan_sana"],
        yaratilgan=yozuv["yaratilgan"],
        hudud=yozuv.get("hudud", ""),
    )


def sms_yuborish(xom_telefon: str, xom_sana: str) -> tuple[str, int]:
    """Tasdiqlash kodini yaratadi. Qaytaradi: (kod, amal qilish muddati soniyada).

    ⚠️ MOCK: kod qaytariladi va interfeysda ko'rsatiladi. Haqiqiy SMS ulanganda
    bu yerda kod yuboriladi va qaytarilmaydi.
    """
    telefon = telefonni_tozalash(xom_telefon)
    sana = sanani_tozalash(xom_sana)

    with _qulf:
        baza = _bazani_oqish()
        _tozalash(baza)

        mavjud = baza["kodlar"].get(telefon)
        if mavjud:
            yuborilgan = datetime.fromisoformat(mavjud["yuborilgan"])
            kutish = KOD_QAYTA_YUBORISH_SONIYA - (_hozir() - yuborilgan).total_seconds()
            if kutish > 0:
                raise KirishXatosi("tez_tez")

        # Ro'yxatdan o'tgan foydalanuvchi boshqa tug'ilgan sana kiritsa — kiritmaymiz.
        hisob = baza["foydalanuvchilar"].get(telefon)
        if hisob and hisob["tugilgan_sana"] != sana:
            raise KirishXatosi("sana_mos_emas")

        kod = f"{secrets.randbelow(1_000_000):06d}"
        baza["kodlar"][telefon] = {
            "kod": kod,
            "tugilgan_sana": sana,
            "yuborilgan": _hozir().isoformat(),
            "muddat": (_hozir() + timedelta(seconds=KOD_MUDDATI_SONIYA)).isoformat(),
            "urinishlar": 0,
        }
        _bazani_yozish(baza)

    return kod, KOD_MUDDATI_SONIYA


def tasdiqlash(xom_telefon: str, kod: str, hudud: str = "") -> tuple[Foydalanuvchi, str]:
    """Kodni tekshiradi; to'g'ri bo'lsa hisob ochadi (yoki topadi) va sessiya beradi.

    `hudud` — foydalanuvchi tanlagan viloyat; berilgan bo'lsa hisobda yangilanadi.
    """
    telefon = telefonni_tozalash(xom_telefon)
    kod = re.sub(r"\D", "", kod or "")

    with _qulf:
        baza = _bazani_oqish()
        _tozalash(baza)

        yozuv = baza["kodlar"].get(telefon)
        if not yozuv:
            raise KirishXatosi("kod_eskirgan")

        if yozuv["urinishlar"] >= KOD_URINISHLARI:
            del baza["kodlar"][telefon]
            _bazani_yozish(baza)
            raise KirishXatosi("urinishlar_tugadi")

        if not secrets.compare_digest(kod, yozuv["kod"]):
            yozuv["urinishlar"] += 1
            _bazani_yozish(baza)
            raise KirishXatosi("kod_notogri")

        hisob = baza["foydalanuvchilar"].get(telefon)
        if not hisob:
            hisob = {
                "telefon": telefon,
                "tugilgan_sana": yozuv["tugilgan_sana"],
                "yaratilgan": _hozir().isoformat(),
                "hudud": hudud,
            }
            baza["foydalanuvchilar"][telefon] = hisob
        elif hudud:
            hisob["hudud"] = hudud

        del baza["kodlar"][telefon]
        token = secrets.token_urlsafe(32)
        baza["sessiyalar"][token] = {
            "telefon": telefon,
            "muddat": (_hozir() + timedelta(days=SESSIYA_KUNI)).isoformat(),
        }
        _bazani_yozish(baza)
        return _foydalanuvchi(hisob), token


def sessiya_boyicha(token: str | None) -> Foydalanuvchi | None:
    if not token:
        return None
    baza = _bazani_oqish()
    sessiya = baza["sessiyalar"].get(token)
    if not sessiya:
        return None
    if datetime.fromisoformat(sessiya["muddat"]) < _hozir():
        return None
    yozuv = baza["foydalanuvchilar"].get(sessiya["telefon"])
    return _foydalanuvchi(yozuv) if yozuv else None


def chiqish(token: str | None) -> None:
    if not token:
        return
    with _qulf:
        baza = _bazani_oqish()
        if baza["sessiyalar"].pop(token, None) is not None:
            _bazani_yozish(baza)
