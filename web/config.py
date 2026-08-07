"""Web qismining yo'llari va sozlamalari.

Ataylab `bot.config` dan mustaqil: u BOT_TOKEN/GEMINI_API_KEY talab qiladi va
ularsiz SystemExit bilan to'xtaydi. Katalog va hisoblar esa Gemini kalitisiz
ishlaydi — ularga faqat Postgres (`DATABASE_URL`) kerak.

Katalog ma'lumotlarining o'zi endi bazada; `data/*.json` fayllari faqat bazani
to'ldirish uchun ishlatiladi (`baza/json_manba.py`).
"""

import os
from pathlib import Path

from baza.muhit import env_yuklash

env_yuklash()

LOYIHA_ILDIZI = Path(__file__).resolve().parent.parent

FRONTEND_YOLI = Path(__file__).parent / "frontend"
FRONTEND_DIST_YOLI = FRONTEND_YOLI / "dist"

# Frontend backendsiz ham katalogni ko'rsata olishi uchun eksport qilinadigan fayl
# (web/eksport_katalog.py yozadi, Vite uni /data/katalog.json sifatida beradi).
KATALOG_EKSPORT_YOLI = FRONTEND_YOLI / "public" / "data" / "katalog.json"

# Soat uchun: server vaqti shu mintaqada yuboriladi.
VAQT_MINTAQASI = "Asia/Tashkent"

# ── Sessiya cookie'si ─────────────────────────────────────────────────────────
# Frontend va API bitta domenda bo'lsa (uvicorn statikani ham beradi) standart
# qiymatlar to'g'ri keladi. Frontend alohida domenda bo'lsa (masalan Netlify,
# API esa boshqa xostda) brauzer cookie'ni faqat `SameSite=None; Secure` bilan
# yuboradi — u holda quyidagilarni environment orqali o'zgartiring.
COOKIE_SAMESITE = os.environ.get("COMPASS_COOKIE_SAMESITE", "lax").lower()
COOKIE_SECURE = os.environ.get("COMPASS_COOKIE_SECURE", "").lower() in ("1", "true", "yes")

# ── CORS ──────────────────────────────────────────────────────────────────────
# Vergul bilan ajratilgan manzillar, masalan:
#   COMPASS_RUXSAT_MANBALAR=https://compass.netlify.app,http://localhost:5173
# Bo'sh bo'lsa CORS umuman yoqilmaydi (bitta domenli o'rnatish uchun shart emas).
RUXSAT_ETILGAN_MANBALAR = [
    manzil.strip()
    for manzil in os.environ.get("COMPASS_RUXSAT_MANBALAR", "").split(",")
    if manzil.strip()
]
