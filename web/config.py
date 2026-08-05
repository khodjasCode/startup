"""Web qismining yo'llari va sozlamalari.

Ataylab `bot.config` dan mustaqil: u BOT_TOKEN/GEMINI_API_KEY talab qiladi va
ularsiz SystemExit bilan to'xtaydi. Katalog va hisoblar esa hech
qanday kalitsiz ishlashi kerak (masalan katalogni eksport qilish skriptida).
"""

import os
from pathlib import Path

LOYIHA_ILDIZI = Path(__file__).resolve().parent.parent

DATA_YOLI = LOYIHA_ILDIZI / "data"

BILIM_BAZASI_YOLI = DATA_YOLI / "bilim_bazasi.json"
MY_GOV_YOLI = DATA_YOLI / "my-gov.json"
PM_GOV_YOLI = DATA_YOLI / "pm-gov.json"
LEX_YOLI = DATA_YOLI / "lex.json"
SAVOL_JAVOB_YOLI = DATA_YOLI / "savol-javob.json"

FRONTEND_YOLI = Path(__file__).parent / "frontend"
FRONTEND_DIST_YOLI = FRONTEND_YOLI / "dist"

# Frontend backendsiz ham katalogni ko'rsata olishi uchun eksport qilinadigan fayl
# (web/eksport_katalog.py yozadi, Vite uni /data/katalog.json sifatida beradi).
KATALOG_EKSPORT_YOLI = FRONTEND_YOLI / "public" / "data" / "katalog.json"

FOYDALANUVCHILAR_YOLI = Path(
    os.environ.get("COMPASS_FOYDALANUVCHILAR", LOYIHA_ILDIZI / "foydalanuvchilar.json")
)

# Soat uchun: server vaqti shu mintaqada yuboriladi.
VAQT_MINTAQASI = "Asia/Tashkent"
