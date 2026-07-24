# Web qismi — sheriklar uchun yo'riqnoma

Bu fayl `web/` papkasi (brauzer orqali ochiladigan sayt + chat widget)
ustida ishlaydigan sheriklar uchun.

## 1. O'rnatish

```powershell
cd yonaltiruvchi-bot
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`requirements.txt` ichida `fastapi` va `uvicorn` allaqachon bor.

## 2. Kerakli tokenlar (environment variable'lar)

⚠️ **Haqiqiy tokenlarni bu faylga yoki boshqa git'ga tushadigan faylga
yozmang.** Har kim o'z kalitini o'zi oladi yoki jamoa boshlig'idan **shaxsiy**
xabar orqali so'raydi.

| Nomi | Majburiymi | Nima uchun |
|---|---|---|
| `GEMINI_API_KEY` | Ha | Web sahifadagi javoblar ham xuddi bot bilan bir xil `bot/rag.py` orqali ishlaydi |
| `GEMINI_API_KEY_ZAXIRA` | Ixtiyoriy | 429 (limit) bo'lganda avtomatik zaxira kalitga o'tish uchun |
| `BOT_TOKEN` | Ha (garchi ishlatilmasa ham!) | Pastdagi eslatmaga qarang |

> **Muhim eslatma:** web serveri Telegram bilan bog'liq emas, lekin
> `web/main.py` ichida `bot.rag`ni import qilganda, u o'z navbatida
> `bot.config`ni import qiladi — u esa `BOT_TOKEN` mavjudligini **majburiy**
> talab qiladi (`os.environ["BOT_TOKEN"]`). Shu sabab, agar sizda haqiqiy
> Telegram bot tokeni bo'lmasa, `BOT_TOKEN`ga vaqtincha istalgan bo'sh
> bo'lmagan qiymat qo'ying (masalan `test`) — web server uchun bu qiymat
> hech qanday ishlatilmaydi, faqat import xatosining oldini olish uchun kerak.

### Qanday o'rnatish (Windows)

`setx` ISHLATMANG. PowerShell orqali (faqat shu o'zgaruvchi yoziladi):

```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "shu_yerga_kalitni_qoying", "User")
[Environment]::SetEnvironmentVariable("BOT_TOKEN", "test", "User")
```

Yoki GUI: `Win + R` → `sysdm.cpl` → *Advanced* → *Environment Variables* →
*User variables* → *New*. O'zgartirgandan keyin barcha ochiq
terminal/IDE oynalarini yopib qaytadan oching.

## 2b. Joriy tokenlar (hozircha ishlaydigan qiymatlar)

> Bu qiymatlar hozircha ishlaydi, keyinroq almashtiriladi (rotatsiya qilinadi).
> Faqat jamoa a'zolari uchun — boshqa hech kimga yubormang.

```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AQ.Ab8RN6IytB7Ux7H1hxYNA5u5NC8vGiZAc1VTaGkNOkbu8_H4LQ", "User")
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY_ZAXIRA", "AQ.Ab8RN6IZpWchVQUlSyoOZR0C8a1N-OgUBdgjq9ueuhI-CkKJIQ", "User")
[Environment]::SetEnvironmentVariable("BOT_TOKEN", "8930965463:AAE5wrjuzZJm5NRzSYq1glcBRaZZ0S8aFA4", "User")
```

O'rnatgandan keyin barcha ochiq terminal/IDE oynalarini yopib, qaytadan oching.

## 3. Bazani indekslash

Web ham bot bilan **bir xil** ChromaDB bazasidan foydalanadi, shuning uchun
avval baza indekslangan bo'lishi kerak (bot tomondan bir marta qilingan
bo'lsa, qayta qilish shart emas):

```powershell
python -m bot.index_qurish
```

## 4. Serverni ishga tushirish

Repo **root** papkasida turib:

```powershell
uvicorn web.main:app --reload
```

Brauzerda oching: **http://127.0.0.1:8000**

❌ `python web/main.py` deb to'g'ridan-to'g'ri ishga tushirmang —
`web/main.py` ASGI ilova (`app` obyekti), mustaqil skript emas, va faylni
shu tarzda ishga tushirish `bot` paketini topa olmay xato beradi. Faqat
yuqoridagi `uvicorn` buyrug'idan foydalaning.

## 5. Loyiha tuzilishi

- `web/main.py` — FastAPI server:
  - `GET /` → `web/static/homepage.html`
  - `POST /api/savol` → `bot.rag.javob_olish()`ni chaqiradi, `{"javob": "..."}` qaytaradi
  - `/static/*` — `web/static/` papkasidagi barcha fayllar shu orqali ochiladi
- `web/static/homepage.html` — asosiy landing sahifa (my.gov.uz uslubidan ilhomlangan, lekin o'z brendi bilan — kategoriya kartochkalari, pastki-o'ng burchakda chat tugmasi)
- `web/static/widget.html` — chat popup ichidagi UI (iframe orqali yuklanadi)

## 6. Suhbat konteksti (session)

- `widget.html` sahifa yuklanganda `crypto.randomUUID()` bilan tasodifiy `session_id` yaratadi va har bir `/api/savol` so'roviga qo'shib yuboradi.
- Server (`web/main.py`) `session_id` bo'yicha suhbat tarixini xotirada (`SUHBATLAR` lug'ati) saqlaydi — shu tufayli bot "suv chiqmayapti" kabi noaniq savolga aniqlashtiruvchi savol berib, keyingi xabarlar bilan to'ldirilgan javob bera oladi.
- Server qayta ishga tushsa (`--reload` bilan kod o'zgarganda ham) barcha suhbatlar tarixi yo'qoladi — MVP uchun bu normal.

## 7. Bilish kerak bo'lgan narsalar

- `bot/` papkasidagi hech bir faylni web ishi uchun o'zgartirish shart emas — `web/` faqat `bot.rag.javob_olish()`ni tashqaridan chaqiradi.
- Ikkala Gemini kalit ham 429 (limit) qaytarsa, foydalanuvchiga avtomatik chiroyli "so'rov limiti tugadi" xabari chiqadi (`bot/rag.py` dagi `TOKENLAR_TUGADI_XABARI`).
- `homepage.html`da real my.gov.uz'ning nomi, logotipi, schema.org identifikatori yoki haqiqiy JS bundle'lari ISHLATILMAGAN — bu ataylab shunday qilingan (impersonatsiya xavfi tufayli). Vizual uslub (ranglar, layout) ilhomlangan bo'lishi mumkin, lekin real tashkilot identifikatorini qo'shmang.
