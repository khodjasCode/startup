"""Telegram webhook'ini ro'yxatdan o'tkazish / o'chirish / holatini ko'rish.

Ishga tushirish (repo ildizidan):

    python3 -m web.telegram_webhook              # holatni ko'rsatadi
    python3 -m web.telegram_webhook --ornatish   # webhook'ni o'rnatadi
    python3 -m web.telegram_webhook --ochirish   # webhook'ni olib tashlaydi
                                                 # (long polling'ga qaytish uchun)

Kerakli environment o'zgaruvchilari:
    BOT_TOKEN                 — bot kaliti
    COMPASS_PUBLIC_URL        — servisning ochiq manzili, masalan
                                https://compass-api-x8uy.onrender.com
    TELEGRAM_WEBHOOK_SECRET   — maxfiy qiymat; Telegram uni har so'rovda
                                sarlavhada qaytaradi (web/api/telegram.py)

⚠️ Telegram bir vaqtda faqat bitta usulni qo'llaydi: webhook o'rnatilgan
bo'lsa `python3 -m bot.main` (polling) ishlamaydi va aksincha.
"""

import json
import os
import sys
import urllib.request

from baza.muhit import env_yuklash

env_yuklash()

YOL = "/telegram/webhook"


def _kalit(nom: str) -> str:
    qiymat = os.environ.get(nom, "").strip()
    if not qiymat:
        raise SystemExit(f"XATO: {nom} topilmadi (.env yoki environment orqali bering).")
    return qiymat


def _sorov(usul: str, **parametrlar) -> dict:
    manzil = f"https://api.telegram.org/bot{_kalit('BOT_TOKEN')}/{usul}"
    tana = json.dumps(parametrlar).encode("utf-8")
    sorov = urllib.request.Request(
        manzil, data=tana, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(sorov, timeout=30) as javob:
        return json.loads(javob.read())


def holat() -> dict:
    return _sorov("getWebhookInfo")["result"]


def ornatish() -> dict:
    manzil = _kalit("COMPASS_PUBLIC_URL").rstrip("/") + YOL
    natija = _sorov(
        "setWebhook",
        url=manzil,
        secret_token=_kalit("TELEGRAM_WEBHOOK_SECRET"),
        allowed_updates=["message", "callback_query"],
        # Servis uxlab qolgan paytdagi eski xabarlar to'planib qolmasin.
        drop_pending_updates=True,
    )
    print(f"o'rnatildi: {manzil}" if natija.get("ok") else natija)
    return natija


def ochirish() -> dict:
    natija = _sorov("deleteWebhook", drop_pending_updates=False)
    print("o'chirildi" if natija.get("ok") else natija)
    return natija


def main() -> None:
    bayroqlar = set(sys.argv[1:])
    if "--ornatish" in bayroqlar:
        ornatish()
    elif "--ochirish" in bayroqlar:
        ochirish()

    joriy = holat()
    print("Webhook holati:")
    for kalit in ("url", "pending_update_count", "last_error_message", "last_error_date"):
        if kalit in joriy:
            print(f"  {kalit:<22} {joriy[kalit]}")
    if not joriy.get("url"):
        print("  (webhook o'rnatilmagan — bot faqat `python3 -m bot.main` bilan ishlaydi)")


if __name__ == "__main__":
    main()
