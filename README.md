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
 2) Postgres'dan top-3     → bot/rag.py (pgvector)
 3) yozuvlar + savol → LLM → bot/rag.py + bot/prompt.py
 4) javob + manba          → foydalanuvchiga
```

## Loyiha tuzilishi

```
bot/
  main.py         — Telegram bot (aiogram 3, long polling), kirish nuqtasi
  rag.py          — RAG yadro: qidirish + javob olish (Gemini, pgvector)
  index_qurish.py — bilim bazasini vektor jadvaliga indekslash skripti
  prompt.py       — qat'iy system prompt (gallyutsinatsiyaga qarshi)
  config.py       — kalitlar (env), yo'llar, model nomlari
data/
  bilim_bazasi.json — RAG bilim bazasi (muammo → idora yozuvlari)
qa/
  test_savollar.json    — 40 ta test-savol (30 oddiy + 10 "tuzoq")
  baholash.py           — sifatni avtomatik baholash, hisobot chiqaradi
  foydalanuvchi_testi.md — real foydalanuvchi sinovi rejasi va bug ro'yxati
  demo_ssenariy.md      — demo ssenariy va slaydlar rejasi
docs/
  ISH_REJA.md     — 4 haftalik ish reja
baza/
  __init__.py     — PostgreSQL ulanishi (hovuz, so'rov yordamchilari)
  sxema.sql       — jadvallar
  kochirish.py    — sxema + data/*.json dan katalogni bazaga yuklash
  json_manba.py   — data/*.json → bazaga yoziladigan qatorlar
  suhbat.py       — suhbat tarixi (web va Telegram uchun umumiy)
web/
  main.py         — FastAPI ilovasi (routerlar + yig'ilgan frontendni tarqatish)
  api/            — HTTP: chat, katalog, avtorizatsiya, vaqt (soat)
  xizmat/         — xizmat qatlami: katalog bazasi, foydalanuvchi hisoblari
  frontend/       — React + TS ilova (app → pages → features → shared)
```

## Ishga tushirish

```bash
pip3 install -r requirements.txt

cp .env.example .env         # so'ng .env ichiga kalitlarni yozing:
                             #   BOT_TOKEN — BotFather'dan
                             #   GEMINI_API_KEY — https://ai.google.dev dan
                             #   DATABASE_URL — PostgreSQL (Supabase) manzili
                             # (.env o'zi yuklanadi, export shart emas)

python3 -m baza.kochirish    # jadvallar + katalogni bazaga yuklash (bir marta)
python3 -m bot.index_qurish  # vektor indeksni qurish (bir marta / baza yangilanganda)
python3 -m bot.main          # botni ishga tushirish
```

## Ma'lumotlar bazasi (PostgreSQL / Supabase)

Katalog, foydalanuvchi hisoblari, sessiyalar va suhbat tarixi Postgres'da
saqlanadi. `data/*.json` fayllari manba (source of truth) bo'lib qoladi:
ular o'zgargach baza qayta yuklanadi.

```bash
python3 -m baza.kochirish            # sxema + katalog + tarjimalar + eski hisoblar
python3 -m baza.kochirish --sxema    # faqat jadvallarni yaratish
python3 -m baza.kochirish --holat    # jadvallardagi yozuvlar soni
```

| Jadval | Nima saqlanadi |
|---|---|
| `xizmatlar`, `manbalar` | katalog: xizmatlar, savol-javoblar, portallar |
| `tarjimalar` | ru/en tarjimalari (`data/i18n/*.json` dan) |
| `foydalanuvchilar`, `sessiyalar`, `kirish_kodlari` | telefon orqali kirish |
| `suhbat_xabarlari`, `telegram_foydalanuvchilari` | chat tarixi va tanlangan til |
| `vektorlar` | RAG qidiruvi uchun embedding'lar (pgvector) |

Katalog kamdan-kam o'zgaradi, shuning uchun u xotirada keshlanadi
(`COMPASS_KATALOG_KESH_SONIYA`, standart 300 soniya; `0` — keshsiz).
Ulanishni tekshirish: `curl http://127.0.0.1:8000/api/salomatlik`.

## Web-versiya

Bir xil `bot/rag.py` yadrosidan foydalanadigan sayt + chat widget. Interfeys —
React + TypeScript (Vite), FastAPI uni yig'ilgan holda tarqatadi:

```bash
python3 -m baza.kochirish                         # bir marta: bazani to'ldirish
cd web/frontend && npm install && npm run build   # bir marta (Node.js 20+)
cd ../.. && uvicorn web.main:app --reload         # http://127.0.0.1:8000
```

Faqat interfeys ustida ishlaganda qayta yig'ish shart emas — `npm run dev`
(5173-port) `/api` so'rovlarini uvicorn'ga proksilaydi.

Saytda: kategoriyalar va xizmatlar katalogi (329 yozuv), manbalar, savol-javob
bo'limi, hisob ochish/kirish, mavzu (yorug'/qorong'i) va til tanlash.
Chat har sahifadan ochiladi va butun ekranga yoyiladi.

`BOT_TOKEN`/`GEMINI_API_KEY` bot bilan bir xil environment variable'lardan o'qiladi — alohida sozlash shart emas, faqat baza avval indekslangan bo'lishi kerak (`python -m bot.index_qurish`).

Batafsil (arxitektura va qatlam qoidalari): [instructions/WEB.md](instructions/WEB.md)

## Sifatni tekshirish (QA)

```bash
python3 -m qa.baholash          # qidiruv aniqligi, ~30 soniya (BOT_TOKEN kerak emas)
python3 -m qa.baholash --javob  # + tuzoq savollarga LLM javoblari (~3 daqiqa, bepul limit sekin)
```

Natija `qa/hisobot_YYYY-MM-DD.md` faylga yoziladi.
