# Gemini API kalitlari

Joriy ishlaydigan Gemini API kalitlar ro'yxati. `bot/rag.py` ularni shu
tartibda ishlatadi: birinchisi 429 (so'rov limiti) qaytarsa, avtomatik
navbatdagisiga o'tiladi (`_kalitlar_bilan_urin`).

⚠️ **Haqiqiy kalitlarni bu fayldan tashqari hech qanday git'ga tushadigan
faylga yozmang** — bu fayl allaqachon repo tarkibida, shuning uchun faqat
shu yerda saqlanadi; ishchi muhitda esa `.env` fayliga yoziladi (u
`.gitignore`da, git'ga tushmaydi).

| Env o'zgaruvchi | Qiymat |
|---|---|
| `GEMINI_API_KEY` | `AQ.Ab8RN6IytB7Ux7H1hxYNA5u5NC8vGiZAc1VTaGkNOkbu8_H4LQ` |
| `GEMINI_API_KEY_ZAXIRA` | `AQ.Ab8RN6IZpWchVQUlSyoOZR0C8a1N-OgUBdgjq9ueuhI-CkKJIQ` |
| `GEMINI_API_KEY_ZAXIRA_2` | `AQ.Ab8RN6KIgArU9THIScS558F285JgZU9BmI776YPWYPKzInwOsA` |
| `GEMINI_API_KEY_ZAXIRA_3` | `AQ.Ab8RN6IMVlw861E8DBW6Zm4eN6O08O9OYqgRfGnECqrfPvO99A` |
| `GEMINI_API_KEY_ZAXIRA_4` | `AQ.Ab8RN6IQQ-6QICFD9LmPyFezndbq6LyNxm582nviJnb92yn_cA` |

## .env fayliga qo'shish (terminal, loyiha ildizida)

```
Add-Content .env "GEMINI_API_KEY_ZAXIRA_2=AQ.Ab8RN6KIgArU9THIScS558F285JgZU9BmI776YPWYPKzInwOsA"
Add-Content .env "GEMINI_API_KEY_ZAXIRA_3=AQ.Ab8RN6IMVlw861E8DBW6Zm4eN6O08O9OYqgRfGnECqrfPvO99A"
Add-Content .env "GEMINI_API_KEY_ZAXIRA_4=AQ.Ab8RN6IQQ-6QICFD9LmPyFezndbq6LyNxm582nviJnb92yn_cA"
```

`GEMINI_API_KEY` va `GEMINI_API_KEY_ZAXIRA` allaqachon `.env`da bo'lishi
kerak (qo'yilmagan bo'lsa, `instructions/BOT.md` 2b-bo'limiga qarang).

## Yangi zaxira kalit qo'shish

Yana bir kalit qo'shmoqchi bo'lsangiz: `bot/config.py`da
`GEMINI_API_KEY_ZAXIRA_5` qatorini qo'shing va `bot/rag.py`dagi
`_KALITLAR` ro'yxatiga uni ham kiriting.
