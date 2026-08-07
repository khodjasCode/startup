"""Bazani tayyorlash: sxema + `data/*.json` dan katalogni yuklash.

Ishga tushirish (repo ildizidan):

    python3 -m baza.kochirish              # sxema + katalog + tarjimalar + hisoblar
    python3 -m baza.kochirish --sxema      # faqat jadvallarni yaratish
    python3 -m baza.kochirish --holat      # bazadagi yozuvlar sonini ko'rsatish

Qayta-qayta bajarish xavfsiz: yozuvlar id bo'yicha yangilanadi, JSON'da
qolmagan eski yozuvlar esa o'chiriladi.

Eski `foydalanuvchilar.json` fayli topilsa, undagi hisoblar va sessiyalar bir
marta bazaga ko'chiriladi (mavjud yozuvlar ustiga yozilmaydi).
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from psycopg2.extras import Json, execute_values

from baza import bitta, sorov, sxemani_yaratish, ulanish
from baza import json_manba
from baza.muhit import LOYIHA_ILDIZI

# Eski JSON hisoblar fayli (endi faqat bir martalik ko'chirish uchun kerak).
ESKI_HISOBLAR_YOLI = Path(
    os.environ.get("COMPASS_FOYDALANUVCHILAR", str(LOYIHA_ILDIZI / "foydalanuvchilar.json"))
)

XIZMAT_USTUNLARI = (
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
    "tartib",
)

MANBA_USTUNLARI = (
    "kalit",
    "nomi",
    "url",
    "tavsif",
    "aloqa",
    "kirish_tartibi",
    "yigilgan_sana",
    "xizmatlar_soni",
    "tartib",
)

# jsonb ustunlari — psycopg2 ro'yxatni o'zi jsonb'ga aylantirmaydi, `Json` kerak.
JSONB_USTUNLARI = {"muammolar", "qadamlar", "hujjatlar", "kirish_tartibi"}


def _qator(yozuv: dict, ustunlar: tuple[str, ...]) -> tuple:
    return tuple(
        Json(yozuv[ustun]) if ustun in JSONB_USTUNLARI else yozuv[ustun] for ustun in ustunlar
    )


def _yangilash_qismi(ustunlar: tuple[str, ...], kalit: str) -> str:
    """`on conflict do update` uchun `ustun = excluded.ustun, ...`."""
    return ", ".join(f"{u} = excluded.{u}" for u in ustunlar if u != kalit)


def katalogni_yuklash() -> dict:
    xizmatlar, manbalar = json_manba.katalog()
    tarjima_qatorlari = json_manba.tarjimalar()

    if not xizmatlar:
        raise SystemExit(
            "XATO: data/*.json fayllaridan bironta yozuv o'qilmadi — "
            f"{json_manba.DATA_YOLI} papkasini tekshiring."
        )

    with ulanish() as conn:
        with conn.cursor() as cur:
            execute_values(
                cur,
                f"insert into xizmatlar ({', '.join(XIZMAT_USTUNLARI)}) values %s "
                f"on conflict (id) do update set "
                f"{_yangilash_qismi(XIZMAT_USTUNLARI, 'id')}, yangilangan = now()",
                [_qator(x, XIZMAT_USTUNLARI) for x in xizmatlar],
                page_size=200,
            )
            cur.execute(
                "delete from xizmatlar where not (id = any(%s))",
                ([x["id"] for x in xizmatlar],),
            )
            ortiqcha_xizmat = cur.rowcount

            execute_values(
                cur,
                f"insert into manbalar ({', '.join(MANBA_USTUNLARI)}) values %s "
                f"on conflict (kalit) do update set "
                f"{_yangilash_qismi(MANBA_USTUNLARI, 'kalit')}, yangilangan = now()",
                [_qator(m, MANBA_USTUNLARI) for m in manbalar],
            )
            cur.execute(
                "delete from manbalar where not (kalit = any(%s))",
                ([m["kalit"] for m in manbalar],),
            )
            ortiqcha_manba = cur.rowcount

            if tarjima_qatorlari:
                execute_values(
                    cur,
                    "insert into tarjimalar (tur, kalit, til, qiymat) values %s "
                    "on conflict (tur, kalit, til) do update set qiymat = excluded.qiymat",
                    [
                        (t["tur"], t["kalit"], t["til"], Json(t["qiymat"]))
                        for t in tarjima_qatorlari
                    ],
                    page_size=200,
                )

    return {
        "xizmatlar": len(xizmatlar),
        "manbalar": len(manbalar),
        "tarjimalar": len(tarjima_qatorlari),
        "ochirilgan": ortiqcha_xizmat + ortiqcha_manba,
    }


def _sana(xom: str) -> str | None:
    """`yyyy-mm-dd` yoki ISO vaqt → `yyyy-mm-dd`."""
    xom = (xom or "").strip()
    if not xom:
        return None
    return xom[:10]


def eski_hisoblarni_kochirish() -> dict:
    """`foydalanuvchilar.json` → `foydalanuvchilar` va `sessiyalar` jadvallari."""
    if not ESKI_HISOBLAR_YOLI.is_file():
        return {"fayl": None}

    try:
        xom = json.loads(ESKI_HISOBLAR_YOLI.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as xato:
        print(f"⚠️  {ESKI_HISOBLAR_YOLI} o'qilmadi ({xato}) — o'tkazib yuborildi.")
        return {"fayl": str(ESKI_HISOBLAR_YOLI), "foydalanuvchilar": 0, "sessiyalar": 0}

    hisoblar = [
        (
            h["telefon"],
            _sana(h.get("tugilgan_sana", "")),
            h.get("hudud", ""),
            h.get("yaratilgan") or datetime.now(timezone.utc).isoformat(),
        )
        for h in (xom.get("foydalanuvchilar") or {}).values()
        if h.get("telefon") and _sana(h.get("tugilgan_sana", ""))
    ]
    sessiyalar = [
        (token, s["telefon"], s["muddat"])
        for token, s in (xom.get("sessiyalar") or {}).items()
        if s.get("telefon") and s.get("muddat")
    ]

    if not hisoblar:
        return {"fayl": str(ESKI_HISOBLAR_YOLI), "foydalanuvchilar": 0, "sessiyalar": 0}

    with ulanish() as conn:
        with conn.cursor() as cur:
            execute_values(
                cur,
                "insert into foydalanuvchilar (telefon, tugilgan_sana, hudud, yaratilgan) "
                "values %s on conflict (telefon) do nothing",
                hisoblar,
            )
            if sessiyalar:
                # Hisobsiz qolgan sessiya bo'lmasligi uchun faqat ko'chirilgan
                # telefonlarga tegishlilari yoziladi (chet kalit shuni talab qiladi).
                execute_values(
                    cur,
                    "insert into sessiyalar (token, telefon, muddat) "
                    "select v.token, v.telefon, v.muddat::timestamptz from (values %s) "
                    "as v (token, telefon, muddat) "
                    "join foydalanuvchilar f on f.telefon = v.telefon "
                    "on conflict (token) do nothing",
                    sessiyalar,
                )

    return {
        "fayl": str(ESKI_HISOBLAR_YOLI),
        "foydalanuvchilar": len(hisoblar),
        "sessiyalar": len(sessiyalar),
    }


def holat() -> dict:
    """Bazadagi asosiy jadvallar bo'yicha yozuvlar soni."""
    jadvallar = (
        "xizmatlar",
        "manbalar",
        "tarjimalar",
        "foydalanuvchilar",
        "sessiyalar",
        "kirish_kodlari",
        "suhbat_xabarlari",
    )
    natija = {}
    for jadval in jadvallar:
        qator = bitta(f"select count(*) as soni from {jadval}")
        natija[jadval] = qator["soni"] if qator else 0
    return natija


def main() -> None:
    bayroqlar = set(sys.argv[1:])

    if "--holat" in bayroqlar:
        for jadval, soni in holat().items():
            print(f"  {jadval:<20} {soni}")
        return

    print("Sxema tekshirilmoqda…", flush=True)
    sxemani_yaratish()
    print("  ✔ jadvallar joyida")

    if "--sxema" in bayroqlar:
        return

    print("Katalog yuklanmoqda (data/*.json → postgres)…", flush=True)
    natija = katalogni_yuklash()
    print(
        f"  ✔ {natija['xizmatlar']} xizmat, {natija['manbalar']} manba, "
        f"{natija['tarjimalar']} tarjima"
        + (f", {natija['ochirilgan']} eski yozuv o'chirildi" if natija["ochirilgan"] else "")
    )

    hisob = eski_hisoblarni_kochirish()
    if hisob.get("fayl"):
        print(
            f"  ✔ eski hisoblar: {hisob['foydalanuvchilar']} foydalanuvchi, "
            f"{hisob['sessiyalar']} sessiya ({hisob['fayl']})"
        )

    sohalar = sorov("select count(distinct soha) as soni from xizmatlar where not faq")
    print(f"\nTayyor. Sohalar: {sohalar[0]['soni']}.")


if __name__ == "__main__":
    main()
