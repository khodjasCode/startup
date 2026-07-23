# Bot qismi — sheriklar uchun yo'riqnoma

Bu fayl `bot/` papkasi (Telegram bot) ustida ishlaydigan sheriklar uchun.

## 1. O'rnatish

```powershell
cd yonaltiruvchi-bot
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Kerakli tokenlar (environment variable'lar)

⚠️ **Haqiqiy tokenlar bu faylga yoki boshqa hech qanday git'ga tushadigan
faylga yozilmaydi va yozilmasligi kerak** — ular git tarixida abadiy qolib
ketadi, hatto keyinroq o'chirilsa ham. Har kim o'z tokenini o'zi oladi yoki
jamoa boshlig'idan **shaxsiy** xabar orqali so'raydi (guruh chatida emas).

| Nomi | Majburiymi | Nima uchun | Qayerdan olinadi |
|---|---|---|---|
| `BOT_TOKEN` | Ha | Telegram bot tokeni | [@BotFather](https://t.me/BotFather) — asosiy botni ishga tushirish uchun jamoa boshlig'idagi tokendan foydalaning, shaxsiy test uchun `/newbot` bilan o'zingiznikini yarating |
| `GEMINI_API_KEY` | Ha | Gemini embedding + LLM uchun asosiy kalit | https://ai.google.dev (AI Studio) — bepul, o'zingiz ham yarata olasiz |
| `GEMINI_API_KEY_ZAXIRA` | Ixtiyoriy | Asosiy kalit so'rov limitiga (429) yetsa, avtomatik shunga o'tiladi | https://ai.google.dev — boshqa Google hisobida yarating |

### Qanday o'rnatish (Windows)

`setx` buyrug'ini ISHLATMANG — u PATH o'zgaruvchisini buzib qo'yishi mumkin.
Buning o'rniga:

**GUI orqali:** `Win + R` → `sysdm.cpl` → *Advanced* → *Environment Variables*
→ "User variables" bo'limida *New* → nom va qiymatni kiriting → barcha ochiq
terminal/IDE oynalarini yopib, qaytadan oching (eski oynalarda ko'rinmaydi).

**PowerShell orqali** (faqat shu bitta o'zgaruvchini yozadi, PATH'ga tegmaydi):
```powershell
[Environment]::SetEnvironmentVariable("BOT_TOKEN", "shu_yerga_tokeningizni_qoying", "User")
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "shu_yerga_kalitni_qoying", "User")
```

## 2b. Joriy tokenlar (hozircha ishlaydigan qiymatlar)

> Bu qiymatlar hozircha ishlaydi, keyinroq almashtiriladi (rotatsiya qilinadi).
> Faqat jamoa a'zolari uchun — boshqa hech kimga yubormang.

```powershell
[Environment]::SetEnvironmentVariable("BOT_TOKEN", "8930965463:AAE5wrjuzZJm5NRzSYq1glcBRaZZ0S8aFA4", "User")
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AQ.Ab8RN6IytB7Ux7H1hxYNA5u5NC8vGiZAc1VTaGkNOkbu8_H4LQ", "User")
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY_ZAXIRA", "AQ.Ab8RN6IZpWchVQUlSyoOZR0C8a1N-OgUBdgjq9ueuhI-CkKJIQ", "User")
```

O'rnatgandan keyin barcha ochiq terminal/IDE oynalarini yopib, qaytadan oching.

## 3. Bazani indekslash

`data/bilim_bazasi.json` yangilanganda yoki birinchi marta ishga tushirishda:

```powershell
python -m bot.index_qurish
```

## 4. Botni ishga tushirish

Repo **root** papkasida turib:

```powershell
python -m bot.main
```

❌ `python bot/main.py` yoki faylni to'g'ridan-to'g'ri yo'l orqali ishga
tushirmang — `ModuleNotFoundError: No module named 'bot'` xatosini beradi,
chunki bu holda Python `sys.path`ga faylning o'zi joylashgan papkani
qo'shadi, repo root'ni emas. Faqat yuqoridagi `-m bot.main` shaklidan
foydalaning.

## 5. Loyiha tuzilishi

- `bot/main.py` — kirish nuqtasi (aiogram 3, long polling), har chat uchun suhbat tarixini xotirada saqlaydi
- `bot/rag.py` — RAG yadro: savol → embedding → ChromaDB top-3 → Gemini javob; ikkita kalit orasida 429 fallback bilan ishlaydi
- `bot/prompt.py` — system prompt: gallyutsinatsiyaga qarshi qoidalar, aniqlashtiruvchi savol berish mantig'i, javob formati (Markdown emas, emoji-sarlavhali)
- `bot/config.py` — barcha environment variable'lar shu yerdan o'qiladi
- `bot/index_qurish.py` — `data/bilim_bazasi.json`ni ChromaDB'ga yuklovchi skript

## 6. Bilish kerak bo'lgan narsalar

- Suhbat tarixi hozircha **xotirada** saqlanadi — bot qayta ishga tushsa yo'qoladi (MVP uchun yetarli, keyinchalik DB kerak bo'lishi mumkin).
- Bot noaniq savollarga ("suv chiqmayapti") darhol javob bermaydi — avval hudud/muddat kabi aniqlashtiruvchi savol beradi, keyin to'liq javob qaytaradi.
- Ikkala Gemini kalit ham 429 (limit) qaytarsa, foydalanuvchiga avtomatik "so'rov limiti tugadi, xohlasangiz homiylik qiling" xabari chiqadi — bu `bot/rag.py` dagi `TOKENLAR_TUGADI_XABARI` da.
- `data/bilim_bazasi.json`dagi yozuvlarning aksariyati hali `"tekshirilgan": false` — rasmiy manbadan tasdiqlanmagan (telefon/manzil "TEKSHIRILSIN" deb belgilangan). Yangi yozuv qo'shsangiz shu maydonlarni to'ldiring.
