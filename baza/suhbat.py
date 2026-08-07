"""Suhbat holati Postgres'da: web chat va Telegram bot uchun umumiy.

Ilgari tarix jarayon xotirasida (`dict`) saqlanardi va server/bot qayta ishga
tushganda yo'qolardi. Endi u `suhbat_xabarlari` jadvalida: `kanal` — 'web' yoki
'telegram', `sessiya_id` — brauzerdagi suhbat id'si yoki Telegram chat id.

Tarix aniqlashtiruvchi savol-javob oqimi uchun kerak, shuning uchun RAG'ga
faqat so'nggi `TARIX_UZUNLIGI` ta xabar beriladi.

Shu yerda Telegram foydalanuvchisi tanlagan javob tili ham saqlanadi — u ham
bot qayta ishga tushganda yo'qolmasligi kerak.
"""

from __future__ import annotations

import baza

TARIX_UZUNLIGI = 8  # so'nggi N ta xabar (fuqaro+bot) modelga beriladi

WEB = "web"
TELEGRAM = "telegram"


def tarix(sessiya_id: str, kanal: str = WEB, chegara: int = TARIX_UZUNLIGI) -> list[dict]:
    """So'nggi xabarlar, eskisidan yangisiga: `[{"rol": ..., "matn": ...}, ...]`."""
    if not sessiya_id:
        return []
    qatorlar = baza.sorov(
        "select rol, matn from ("
        "  select id, rol, matn from suhbat_xabarlari"
        "  where kanal = %s and sessiya_id = %s order by id desc limit %s"
        ") oxirgilar order by id",
        (kanal, str(sessiya_id), chegara),
    )
    return [{"rol": q["rol"], "matn": q["matn"]} for q in qatorlar]


def saqlash(
    sessiya_id: str,
    savol: str,
    javob: str,
    til: str = "uz",
    kanal: str = WEB,
) -> None:
    """Savol va javobni birga yozadi.

    Ikkalasi bitta tranzaksiyada: javob olinmagan savol tarixda qolib ketmasligi
    kerak (aks holda keyingi savolga kontekst noto'g'ri yig'iladi).
    """
    if not sessiya_id:
        return
    with baza.ulanish() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "insert into suhbat_xabarlari (sessiya_id, kanal, rol, matn, til) "
                "values (%s, %s, %s, %s, %s)",
                [
                    (str(sessiya_id), kanal, "fuqaro", savol, til),
                    (str(sessiya_id), kanal, "bot", javob, til),
                ],
            )


def tozalash(sessiya_id: str, kanal: str = WEB) -> int:
    """Suhbat tarixini o'chiradi (chatdagi "tozalash" tugmasi)."""
    if not sessiya_id:
        return 0
    return baza.bajarish(
        "delete from suhbat_xabarlari where kanal = %s and sessiya_id = %s",
        (kanal, str(sessiya_id)),
    )


# ── Telegram: tanlangan javob tili ────────────────────────────────────────────


def telegram_tili(chat_id: int, standart: str = "uz") -> str:
    qator = baza.bitta(
        "select til from telegram_foydalanuvchilari where chat_id = %s", (chat_id,)
    )
    return qator["til"] if qator else standart


def telegram_tilini_saqlash(chat_id: int, til: str) -> None:
    baza.bajarish(
        "insert into telegram_foydalanuvchilari (chat_id, til) values (%s, %s) "
        "on conflict (chat_id) do update set til = excluded.til, yangilangan = now()",
        (chat_id, til),
    )
