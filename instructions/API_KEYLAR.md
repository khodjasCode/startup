# Gemini API kalitlari

`bot/rag.py` mavjud kalitlarni shu tartibda ishlatadi: birinchisi 429
(so'rov limiti) yoki boshqa xato qaytarsa, avtomatik navbatdagisiga
o'tiladi (`_kalitlar_bilan_urin`).

⚠️ **Haqiqiy kalit qiymatlarini HECH QACHON, HECH QANDAY git'ga tushadigan
faylga yozmang — bu fayl ham shu jumladan.** Bir marta bu faylga yozilgan
va push qilingan kalitlar Google'ning avtomatik "leaked key" skaneri
tomonidan daqiqalar ichida bloklangan edi (2026-08-11 voqeasi). Kalitlar
FAQAT `.env` faylida saqlanadi (u `.gitignore`da, git'ga tushmaydi).

| Env o'zgaruvchi | Qiymat |
|---|---|
| `GEMINI_API_KEY` | `.env` faylida (mahalliy yoki serverda) |
| `GEMINI_API_KEY_ZAXIRA` | `.env` faylida |
| `GEMINI_API_KEY_ZAXIRA_2` | `.env` faylida (ixtiyoriy) |
| `GEMINI_API_KEY_ZAXIRA_3` | `.env` faylida (ixtiyoriy) |
| `GEMINI_API_KEY_ZAXIRA_4` | `.env` faylida (ixtiyoriy) |

Haqiqiy qiymatlarni kim bilishi kerak bo'lsa, ularni git'dan tashqari bir
kanal orqali (masalan to'g'ridan-to'g'ri xabar) yuboring — hech qachon
commit yoki PR orqali emas.

## Yangi kalit olish

https://aistudio.google.com/apikey dan yarating. Yangi kalitlar `AQ.`
prefiksli "auth key" formatida bo'ladi (eski `AIza...` "standard key"
2026-sentabrda butunlay o'chiriladi) — bu normal, muammo emas.

Yangi kalitni sinash (ishlashini tasdiqlash uchun, real qiymat bilan,
lekin faylga yozmasdan):

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: SIZNING_KALIT' \
  -X POST \
  -d '{"contents":[{"parts":[{"text":"salom"}]}]}'
```

## .env fayliga qo'shish (terminal, loyiha ildizida)

```
Add-Content .env "GEMINI_API_KEY=..."
Add-Content .env "GEMINI_API_KEY_ZAXIRA=..."
```

## Yangi zaxira kalit qo'shish (kod tomoni)

Yana bir kalit qo'shmoqchi bo'lsangiz: `bot/config.py`da
`GEMINI_API_KEY_ZAXIRA_5` qatorini qo'shing va `bot/rag.py`dagi
`_KALITLAR` ro'yxatiga uni ham kiriting — qiymatning o'zi faqat `.env`ga
yoziladi.
