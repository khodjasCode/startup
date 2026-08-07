# Konfiguratsiya: kalitlar .env fayldan yoki environment variable orqali (kodga yozmang!)
# BotFather'dan BOT_TOKEN, https://ai.google.dev dan GEMINI_API_KEY

import os
from pathlib import Path

from baza.muhit import env_yuklash

LOYIHA_ILDIZI = Path(__file__).resolve().parent.parent

# .env faylini (bo'lsa) avtomatik yuklash — export qilingan o'zgaruvchilar ustun turadi
env_yuklash()


def _kalit(nom: str) -> str:
    qiymat = os.environ.get(nom, "")
    if not qiymat:
        raise SystemExit(
            f"XATO: {nom} topilmadi. Loyiha ildizidagi .env faylga yozing "
            f"(namuna: .env.example) yoki `export {nom}=...` qiling."
        )
    return qiymat


BOT_TOKEN = _kalit("BOT_TOKEN")
GEMINI_API_KEY = _kalit("GEMINI_API_KEY")
# Zaxira kalit (ixtiyoriy) — asosiy kalit 429 (limit) qaytarsa shunga o'tiladi
GEMINI_API_KEY_ZAXIRA = os.environ.get("GEMINI_API_KEY_ZAXIRA")

BILIM_BAZASI_YOLI = LOYIHA_ILDIZI / "data" / "bilim_bazasi.json"
MY_GOV_YOLI = LOYIHA_ILDIZI / "data" / "my-gov.json"
PM_GOV_YOLI = LOYIHA_ILDIZI / "data" / "pm-gov.json"
LEX_YOLI = LOYIHA_ILDIZI / "data" / "lex.json"
SAVOL_JAVOB_YOLI = LOYIHA_ILDIZI / "data" / "savol-javob.json"

EMBEDDING_MODEL = "gemini-embedding-001"  # 2026-07-22: tekshirildi, hali mavjud
LLM_MODEL = "gemini-flash-latest"  # 2026-07-22: gemini-2.5-flash yangi kalitlarga yopilgan, shuning uchun doim joriy flash modelga ishora qiluvchi alias ishlatilmoqda
LLM_ZAXIRA_MODEL = "gemini-flash-lite-latest"  # asosiy model kunlik limitga urilsa ishlatiladi
