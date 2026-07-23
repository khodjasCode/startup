# Yo'naltiruvchi — Davlat xizmatlari navigatori (Telegram-bot, RAG)

Fuqaro muammosini oddiy tilda yozadi — bot RAG bazasidan mos yozuvni topib,
qaysi idoraga, qanday tartibda, qanday hujjatlar bilan murojaat qilishni aytadi
va rasmiy manbaga havola beradi.

To'liq ish reja: [docs/ISH_REJA.md](docs/ISH_REJA.md)

## Arxitektura

```
Foydalanuvchi (Telegram)
        │
     aiogram bot          → bot/main.py
        │
 1) savol → embedding      → bot/rag.py (Gemini)
 2) ChromaDB'dan top-3     → bot/rag.py
 3) yozuvlar + savol → LLM → bot/rag.py + bot/prompt.py
 4) javob + manba          → foydalanuvchiga
```

## Loyiha tuzilishi

```
bot/
  main.py         — Telegram bot (aiogram 3, long polling), kirish nuqtasi
  rag.py          — RAG yadro: qidirish + javob olish (Gemini, ChromaDB)
  index_qurish.py — bilim bazasini ChromaDB ga indekslash skripti
  prompt.py       — qat'iy system prompt (gallyutsinatsiyaga qarshi)
  config.py       — kalitlar (env), yo'llar, model nomlari
data/
  bilim_bazasi.json — RAG bilim bazasi (muammo → idora yozuvlari)
docs/
  ISH_REJA.md     — 4 haftalik ish reja
```

## Ishga tushirish

```bash
pip install -r requirements.txt

export BOT_TOKEN=...        # BotFather'dan
export GEMINI_API_KEY=...   # https://ai.google.dev dan

python -m bot.index_qurish  # bazani indekslash (bir marta / baza yangilanganda)
python -m bot.main          # botni ishga tushirish
```

## Web-versiya

Bir xil `bot/rag.py` yadrosidan foydalanadigan oddiy web-chat interfeysi (`http://127.0.0.1:8000`):

```bash
uvicorn web.main:app --reload
```

`BOT_TOKEN`/`GEMINI_API_KEY` bot bilan bir xil environment variable'lardan o'qiladi — alohida sozlash shart emas, faqat baza avval indekslangan bo'lishi kerak (`python -m bot.index_qurish`).
