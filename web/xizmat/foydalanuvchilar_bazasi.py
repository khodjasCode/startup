"""Telefon raqami bo'yicha kirish: raqam + tug'ilgan sana → SMS kod → sessiya.

Hozircha SMS **yuborilmaydi**: kod javobning o'zida qaytariladi va interfeysda
ko'rsatiladi (mock). Haqiqiy SMS-provayder ulangach, `sms_yuborish()` dagi
qaytariladigan kodni olib tashlash kifoya — qolgan mantiq o'zgarmaydi.

Ma'lumotlar Postgres'da: `foydalanuvchilar`, `sessiyalar`, `kirish_kodlari`
jadvallari (`baza/sxema.sql`). Bir telefon uchun bir vaqtda bitta amaldagi kod
bo'ladi, shuning uchun kod jadvalining kaliti — telefon raqami.
"""

from __future__ import annotations

import re
import secrets
from dataclasses import dataclass
from datetime import date, datetime, timezone

import baza

SESSIYA_KUNI = 30  # sessiya tokenining amal qilish muddati
KOD_MUDDATI_SONIYA = 300  # SMS kod 5 daqiqa amal qiladi
KOD_QAYTA_YUBORISH_SONIYA = 60  # shu vaqt o'tmasdan yangi kod so'ralmaydi
KOD_URINISHLARI = 5  # noto'g'ri kod kiritishga ruxsat etilgan urinishlar

# O'zbekiston raqami: 998 + 9 raqam.
TELEFON_SHABLONI = re.compile(r"^998\d{9}$")
ENG_KICHIK_YOSH = 14


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


def _sana_matni(qiymat) -> str:
    """`date`/`datetime` → ISO satr (dataclass maydonlari matn saqlaydi)."""
    if qiymat is None:
        return ""
    if isinstance(qiymat, (date, datetime)):
        return qiymat.isoformat()
    return str(qiymat)


def _foydalanuvchi(qator: dict) -> Foydalanuvchi:
    return Foydalanuvchi(
        telefon=qator["telefon"],
        tugilgan_sana=_sana_matni(qator["tugilgan_sana"]),
        yaratilgan=_sana_matni(qator["yaratilgan"]),
        hudud=qator.get("hudud") or "",
    )


def _eskirganlarni_tozalash(cur) -> None:
    """Muddati o'tgan sessiya va kodlarni olib tashlaydi."""
    cur.execute("delete from sessiyalar where muddat < now()")
    cur.execute("delete from kirish_kodlari where muddat < now()")


def sms_yuborish(xom_telefon: str, xom_sana: str) -> tuple[str, int]:
    """Tasdiqlash kodini yaratadi. Qaytaradi: (kod, amal qilish muddati soniyada).

    ⚠️ MOCK: kod qaytariladi va interfeysda ko'rsatiladi. Haqiqiy SMS ulanganda
    bu yerda kod yuboriladi va qaytarilmaydi.
    """
    telefon = telefonni_tozalash(xom_telefon)
    sana = sanani_tozalash(xom_sana)
    kod = f"{secrets.randbelow(1_000_000):06d}"

    with baza.ulanish() as conn:
        with baza.kursor(conn) as cur:
            _eskirganlarni_tozalash(cur)

            cur.execute(
                "select yuborilgan from kirish_kodlari where telefon = %s for update",
                (telefon,),
            )
            mavjud = cur.fetchone()
            if mavjud:
                kutish = (
                    KOD_QAYTA_YUBORISH_SONIYA
                    - (_hozir() - mavjud["yuborilgan"]).total_seconds()
                )
                if kutish > 0:
                    raise KirishXatosi("tez_tez")

            # Ro'yxatdan o'tgan foydalanuvchi boshqa tug'ilgan sana kiritsa — kiritmaymiz.
            cur.execute(
                "select tugilgan_sana from foydalanuvchilar where telefon = %s", (telefon,)
            )
            hisob = cur.fetchone()
            if hisob and _sana_matni(hisob["tugilgan_sana"]) != sana:
                raise KirishXatosi("sana_mos_emas")

            cur.execute(
                "insert into kirish_kodlari "
                "(telefon, kod, tugilgan_sana, yuborilgan, muddat, urinishlar) "
                "values (%s, %s, %s, now(), now() + make_interval(secs => %s), 0) "
                "on conflict (telefon) do update set "
                "kod = excluded.kod, tugilgan_sana = excluded.tugilgan_sana, "
                "yuborilgan = excluded.yuborilgan, muddat = excluded.muddat, urinishlar = 0",
                (telefon, kod, sana, KOD_MUDDATI_SONIYA),
            )

    return kod, KOD_MUDDATI_SONIYA


def tasdiqlash(xom_telefon: str, kod: str, hudud: str = "") -> tuple[Foydalanuvchi, str]:
    """Kodni tekshiradi; to'g'ri bo'lsa hisob ochadi (yoki topadi) va sessiya beradi.

    `hudud` — foydalanuvchi tanlagan viloyat; berilgan bo'lsa hisobda yangilanadi.
    """
    telefon = telefonni_tozalash(xom_telefon)
    kod = re.sub(r"\D", "", kod or "")
    token = secrets.token_urlsafe(32)

    with baza.ulanish() as conn:
        with baza.kursor(conn) as cur:
            _eskirganlarni_tozalash(cur)

            # `for update` — bir vaqtda kelgan ikkita urinish bir-birini bosmasligi uchun.
            cur.execute(
                "select kod, tugilgan_sana, urinishlar from kirish_kodlari "
                "where telefon = %s for update",
                (telefon,),
            )
            yozuv = cur.fetchone()
            if not yozuv:
                raise KirishXatosi("kod_eskirgan")

            if yozuv["urinishlar"] >= KOD_URINISHLARI:
                cur.execute("delete from kirish_kodlari where telefon = %s", (telefon,))
                # Xatolik ko'tarilsa tranzaksiya orqaga qaytadi, shuning uchun
                # o'chirishni alohida saqlaymiz.
                conn.commit()
                raise KirishXatosi("urinishlar_tugadi")

            if not secrets.compare_digest(kod, yozuv["kod"]):
                cur.execute(
                    "update kirish_kodlari set urinishlar = urinishlar + 1 where telefon = %s",
                    (telefon,),
                )
                conn.commit()
                raise KirishXatosi("kod_notogri")

            cur.execute(
                "insert into foydalanuvchilar (telefon, tugilgan_sana, hudud) "
                "values (%s, %s, %s) "
                # Mavjud hisobda hudud faqat yangisi berilgandagina yangilanadi.
                "on conflict (telefon) do update set "
                "hudud = case when %s <> '' then excluded.hudud else foydalanuvchilar.hudud end "
                "returning telefon, tugilgan_sana, hudud, yaratilgan",
                (telefon, _sana_matni(yozuv["tugilgan_sana"]), hudud, hudud),
            )
            hisob = cur.fetchone()

            cur.execute("delete from kirish_kodlari where telefon = %s", (telefon,))
            cur.execute(
                "insert into sessiyalar (token, telefon, muddat) "
                "values (%s, %s, now() + make_interval(days => %s))",
                (token, telefon, SESSIYA_KUNI),
            )

    return _foydalanuvchi(hisob), token


def sessiya_boyicha(token: str | None) -> Foydalanuvchi | None:
    if not token:
        return None
    qator = baza.bitta(
        "select f.telefon, f.tugilgan_sana, f.hudud, f.yaratilgan "
        "from sessiyalar s join foydalanuvchilar f on f.telefon = s.telefon "
        "where s.token = %s and s.muddat > now()",
        (token,),
    )
    return _foydalanuvchi(qator) if qator else None


def chiqish(token: str | None) -> None:
    if not token:
        return
    baza.bajarish("delete from sessiyalar where token = %s", (token,))
