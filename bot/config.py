# Konfiguratsiya: kalitlar environment variable orqali (kodga yozmang!)
# BotFather'dan BOT_TOKEN, https://ai.google.dev dan GEMINI_API_KEY

import os
from pathlib import Path

BOT_TOKEN = os.environ["BOT_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

LOYIHA_ILDIZI = Path(__file__).resolve().parent.parent
BILIM_BAZASI_YOLI = LOYIHA_ILDIZI / "data" / "bilim_bazasi.json"
VEKTOR_BAZA_YOLI = LOYIHA_ILDIZI / "vektor_baza"

EMBEDDING_MODEL = "gemini-embedding-001"  # joriy nomni ai.google.dev da tekshiring
LLM_MODEL = "gemini-2.5-flash"  # joriy bepul modelni ai.google.dev da tekshiring
