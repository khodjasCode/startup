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

> **Eslatma:** kalitlar faqat **chat** uchun kerak. Sayt (katalog, manbalar,
> savol-javob, kirish/ro'yxat, soat) ularsiz ham to'liq ishlaydi — `bot.rag`
> birinchi savol kelgandagina import qilinadi. `BOT_TOKEN` esa faqat shu
> importda talab qilinadi, shuning uchun chatni sinamoqchi bo'lsangiz unga
> istalgan bo'sh bo'lmagan qiymat (masalan `test`) qo'yish kifoya.

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

## 4. Frontendni yig'ish (Node.js 20+ kerak)

Interfeys — React + TypeScript (Vite bilan yig'iladi). Serverni ishga
tushirishdan oldin bir marta yig'ib olinadi:

```powershell
cd web\frontend
npm install
npm run build
```

Natija `web/frontend/dist` papkasiga tushadi (git'ga tushmaydi) va uni
FastAPI o'zi tarqatadi.

`npm run dev`/`npm run build` oldidan avtomatik ravishda
`python -m web.eksport_katalog` ishlaydi va `data/*.json` ni
`web/frontend/public/data/katalog.json` fayliga yig'adi. Shu tufayli backend
ishga tushirilmagan bo'lsa ham (`ECONNREFUSED`) katalog, manbalar va
savol-javob bo'limlari to'ladi — faqat chat va kirish uchun server kerak. Python topilmasa skript ogohlantirish beradi, lekin yig'ishni
to'xtatmaydi.

## 5. Serverni ishga tushirish

Repo **root** papkasida turib:

```powershell
uvicorn web.main:app --reload
```

Brauzerda oching: **http://127.0.0.1:8000**

❌ `python web/main.py` deb to'g'ridan-to'g'ri ishga tushirmang —
`web/main.py` ASGI ilova (`app` obyekti), mustaqil skript emas, va faylni
shu tarzda ishga tushirish `bot` paketini topa olmay xato beradi. Faqat
yuqoridagi `uvicorn` buyrug'idan foydalaning.

### Faqat interfeys ustida ishlayotgan bo'lsangiz

Har o'zgarishda qayta yig'ish shart emas — ikkita terminal:

```powershell
uvicorn web.main:app --reload        # API, 8000-port
cd web\frontend; npm run dev         # UI, 5173-port (hot reload)
```

Brauzerda **http://127.0.0.1:5173** oching — `/api/*` so'rovlari avtomatik
8000-portga proksilanadi (`vite.config.ts`).

## 6. Loyiha tuzilishi

### Backend (`web/`)

```
web/
  main.py                 — FastAPI ilovasi: routerlar + statik frontend + SPA fallback
  api/                    — HTTP qatlami (faqat so'rov/javob, mantiq yo'q)
      chat.py             — POST /api/savol, POST /api/suhbatni-tozalash
      katalog.py          — GET /api/sohalar, /xizmatlar, /xizmatlar/{id},
                            /manbalar, /savol-javob, /statistika
      auth.py             — POST /api/auth/{royxat,kirish,chiqish}, GET /api/auth/men
      vaqt.py             — GET /api/vaqt, WS /ws/vaqt (Toshkent soati)
  config.py               — yo'llar va sozlamalar (kalitsiz, bot.config'dan mustaqil)
  eksport_katalog.py      — data/*.json → frontend/public/data/katalog.json
  xizmat/                 — xizmat qatlami (HTTP'dan mustaqil)
      katalog_bazasi.py   — data/*.json ni yagona shaklga keltirib o'qish
      foydalanuvchilar_bazasi.py — hisoblar, parol hash'i, sessiyalar
```

`bot.rag` (RAG yadrosi) **faqat birinchi savol kelganda** import qilinadi:
`chromadb` o'rnatilmagan yoki Gemini kaliti yo'q bo'lsa sayt baribir to'liq
ishlaydi, chat esa "hozircha sozlanmagan" degan tushunarli xabar qaytaradi.
Chatni yoqish uchun: `pip install -r requirements.txt` va
`python -m bot.index_qurish`.

Muhim: sayt bo'limlari (Kategoriyalar, Barcha bazalar, Manbalar, Savol-javob)
**bir xil `data/*.json`** fayllardan oziqlanadi — RAG uchun ishlatiladigan
ChromaDB indeksi bu yerda kerak emas, shuning uchun bu sahifalar
`python -m bot.index_qurish` qilinmagan holatda ham ishlaydi.

### Avtorizatsiya

- Parollar PBKDF2-HMAC-SHA256 (200 000 iteratsiya) + har foydalanuvchiga alohida
  "tuz" bilan saqlanadi, ochiq matnda hech qachon yozilmaydi.
- Sessiya tokeni **httpOnly cookie**da (`compass_sessiya`) yuriladi — JavaScript
  uni o'qiy olmaydi.
- Hisoblar `foydalanuvchilar.json` faylida (repo ildizida, `.gitignore`da).
  Yo'lni `COMPASS_FOYDALANUVCHILAR` env bilan almashtirish mumkin (testlarda shunday).
- ⚠️ Bu MVP darajasidagi yechim: bitta server nusxasi uchun. Yuklama ortsa yoki
  bir nechta nusxa ishlasa — haqiqiy bazaga (PostgreSQL) ko'chirish kerak.
  Ishlab chiqarishda cookie'ga `secure=True` ham qo'yiladi (HTTPS ostida).

### Frontend (`web/frontend/`)

Qatlamlar yuqoridan pastga qarab bog'lanadi, teskarisi emas
(`app` → `pages` → `features` → `shared`):

```
src/
  app/          — karkas: App (router), routes.ts, provayderlar, layout
  pages/        — sahifalar: home, categories, services (ro'yxat + kartochka),
                  databases, sources, faq, contact
  features/     — mustaqil funksional bo'laklar:
      chat/               model (holat + API) va ui (widget, launcher, xabarlar)
      catalog/            katalog API'si (+ /data/katalog.json zaxirasi),
                          kategoriya kartochkalari, xizmatlar ro'yxati
      auth/               kirish/ro'yxat modali, foydalanuvchi menyusi
      theme-toggle/       quyosh/oy tugmasi (yorug' ↔ qorong'i)
      language-switcher/  ochiladigan menyu: bayroq + UZB / RU / EN
      clock/              Toshkent soati (WebSocket orqali serverdan)
  shared/       — umumiy qatlam: api (fetch), i18n (uz/ru/en), theme (mavzu),
                  lib (hooklar), ui (Icon, Modal, Page, holatlar), styles (tokenlar)
```

Yo'llar (`app/routes.ts` da, navigatsiya ham shu ro'yxatdan quriladi):
`/`, `/kategoriyalar`, `/xizmatlar`, `/xizmatlar/:id`, `/bazalar`, `/manbalar`,
`/savol-javob`, `/aloqa`.

Qoidalar:
- Tarmoq so'rovlari faqat `shared/api/httpClient.ts` orqali; feature'lar
  `fetch`ni to'g'ridan-to'g'ri chaqirmaydi.
- Ranglar/o'lchamlar faqat `shared/styles/tokens.css` dagi CSS o'zgaruvchilari
  orqali; komponent CSS'ida "xom" rang yozilmaydi. Mavzu `<html data-theme>`
  atributi bilan almashadi.
- Matnlar — faqat `shared/i18n` lug'atlarida. O'zbekcha lug'at referens: unga
  yangi kalit qo'shilsa, TypeScript ru/en da ham talab qiladi.
- Kategoriya misollari RAG'ga **doim o'zbekcha** yuboriladi
  (`features/catalog/model/categories.ts` dagi `query`), ko'rinadigan yorliq
  tarjima qilinsa ham — bilim bazasi o'zbek tilida.

## 7. Suhbat konteksti (session)

- Ilova `crypto.randomUUID()` bilan `session_id` yaratadi va uni
  `sessionStorage`da saqlaydi (tab yopilguncha), har bir `/api/savol`
  so'roviga qo'shib yuboradi.
- Server (`web/main.py`) `session_id` bo'yicha suhbat tarixini xotirada (`SUHBATLAR` lug'ati) saqlaydi — shu tufayli bot "suv chiqmayapti" kabi noaniq savolga aniqlashtiruvchi savol berib, keyingi xabarlar bilan to'ldirilgan javob bera oladi.
- Server qayta ishga tushsa (`--reload` bilan kod o'zgarganda ham) barcha suhbatlar tarixi yo'qoladi — MVP uchun bu normal.

## 8. Bilish kerak bo'lgan narsalar

- `bot/` papkasidagi hech bir faylni web ishi uchun o'zgartirish shart emas — `web/` faqat `bot.rag.javob_olish()`ni tashqaridan chaqiradi.
- Ikkala Gemini kalit ham 429 (limit) qaytarsa, foydalanuvchiga avtomatik chiroyli "so'rov limiti tugadi" xabari chiqadi (`bot/rag.py` dagi `TOKENLAR_TUGADI_XABARI`).
- Saytda real my.gov.uz'ning nomi, logotipi, schema.org identifikatori yoki haqiqiy JS bundle'lari ISHLATILMAGAN — bu ataylab shunday qilingan (impersonatsiya xavfi tufayli). Vizual uslub (ranglar, layout) ilhomlangan bo'lishi mumkin, lekin real tashkilot identifikatorini qo'shmang.
- Chat widget endi alohida iframe emas, oddiy React komponenti — til va suhbat
  holati bosh sahifa bilan yagona manbadan keladi, `postMessage` ko'prigi
  kerak emas. Uchta ko'rinishi bor: oyna (suriladi), kichraytirilgan va butun
  ekran (Escape bilan oynaga qaytadi).
- Yon panel sarlavhadagi bitta ikonka-tugma bilan ochiladi/yopiladi; tanlov
  `localStorage`da eslab qolinadi (kichik ekranda panel doim yopiq ochiladi).
  Panel `position: fixed` — sahifa aylantirilganda joyida qoladi, faqat
  o'rtadagi kontent siljiydi.
- Soat: `/ws/vaqt` har soniyada Toshkent vaqtini yuboradi (O'zbekiston doimiy
  UTC+5, shuning uchun `zoneinfo`/`tzdata` kerak emas). Ulanish uzilsa frontend
  brauzer soatidan hisoblaydi va 5 soniyada qayta ulanishga urinadi; yashil
  nuqta vaqt serverdan kelayotganini bildiradi.
- Chat sarlavhasidagi tugmalar `data-no-drag` ichida: aks holda panelni sudrash
  uchun qo'yilgan pointer capture ularning bosilishini "o'g'irlab" qo'yadi.
- Logotip: `public/images/logo-mark-light.png` (rangli, oq taglikda) va
  `logo-mark-dark.png` (oq chizmali, qorong'i mavzuda) — bular
  `assets/images/{ligt,dark}-logo.png` dan "compass" yozuvi kesib olingan
  nusxalari. Nom yon panelda matn sifatida yoziladi (`--font-brand`), shuning
  uchun u har qanday o'lchamda tiniq ko'rinadi.
- Yon panelning ikki holati bor: yoyilgan (260px, yozuvlar bilan) va yig'ilgan
  tasma (62px, faqat ikonkalar). Yig'ish tugmasi panelning o'zida; tasma
  holatida u yashirinadi va logotip ustiga kursor kelganda uning o'rnida
  paydo bo'ladi. Kichik ekranda esa panel butunlay chetga chiqib ketadi va
  sarlavhadagi tugma bilan ochiladi.
- Yorug' mavzuda panel kulrang-oq (`--sidebar`), chunki ko'k fonda rangli
  logotip yaxshi o'tirmasdi.
