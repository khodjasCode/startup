# Konfiguratsiya: kalitlar environment variable orqali (kodga yozmang!)
# BotFather'dan BOT_TOKEN, https://ai.google.dev dan GEMINI_API_KEY

import os
from pathlib import Path

BOT_TOKEN = os.environ["BOT_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
# Zaxira kalit (ixtiyoriy) — asosiy kalit 429 (limit) qaytarsa shunga o'tiladi
GEMINI_API_KEY_ZAXIRA = os.environ.get("GEMINI_API_KEY_ZAXIRA")

LOYIHA_ILDIZI = Path(__file__).resolve().parent.parent
BILIM_BAZASI_YOLI = LOYIHA_ILDIZI / "data" / "bilim_bazasi.json"
VEKTOR_BAZA_YOLI = LOYIHA_ILDIZI / "vektor_baza"

EMBEDDING_MODEL = "gemini-embedding-001"  # 2026-07-22: tekshirildi, hali mavjud
LLM_MODEL = "gemini-flash-latest"  # 2026-07-22: gemini-2.5-flash yangi kalitlarga yopilgan, shuning uchun doim joriy flash modelga ishora qiluvchi alias ishlatilmoqda
