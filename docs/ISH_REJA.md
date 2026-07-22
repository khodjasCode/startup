# "Yo'naltiruvchi" — Davlat xizmatlari navigatori (Telegram-bot, RAG)

**Muddat:** 4 hafta | **Jamoa:** 2–3 student | **Byudjet:** ~0 so'm

---

## 1. Loyiha qisqacha

Fuqaro muammosini oddiy tilda yozadi ("qo'shnim tomdan suv oqizyapti", "3 oydan beri oylik berishmayapti") — bot RAG bazasidan mos yozuvni topib, **qaysi idoraga, qanday tartibda, qanday hujjatlar bilan** murojaat qilishni aytadi va rasmiy manbaga havola beradi.

**Asosiy qoida (gallyutsinatsiyaga qarshi):** bot faqat bazada bor ma'lumotni aytadi. Bazada yo'q bo'lsa — "aniq ma'lumotim yo'q, umumiy tartib bunday: my.gov.uz yoki Prezident virtual qabulxonasi (pm.gov.uz)" deb javob beradi. Hech qachon idora nomi/telefonini "o'ylab topmaydi".

---

## 2. Texnik stack

| Qism | Tanlov | Nima uchun |
|---|---|---|
| Til | Python 3.11+ | Eng ko'p tutorial, jamoa uchun eng oson |
| Bot framework | aiogram 3 | Zamonaviy, async, yaxshi hujjatlangan |
| LLM | Gemini Flash (bepul tier) | Karta shart emas, o'zbekchani tushunadi |
| Embedding | Gemini embedding modeli (bepul) | Alohida xizmat kerak emas |
| Vektor baza | ChromaDB (lokal) | `pip install` — tamom, server kerak emas |
| Ma'lumot bazasi | JSON fayl(lar) | 30–50 yozuv uchun ortiqcha DB kerak emas |
| Hosting (dev/demo) | O'z kompyuter (long polling) | Bepul, oq IP shart emas |
| Hosting (keyin) | Istalgan arzon VPS yoki bepul tier PaaS | MVP'dan keyingi masala |

**Arxitektura (soddalashtirilgan):**

```
Foydalanuvchi (Telegram)
        │
     aiogram bot
        │
 1) savol → embedding (Gemini)
 2) ChromaDB'dan top-3 mos yozuv
 3) yozuvlar + savol → Gemini Flash (qat'iy system prompt)
 4) javob + manba havolasi → foydalanuvchiga
```

---

## 3. Jamoa rollari (3 kishiga misol)

- **A (backend):** bot skeleti, RAG pipeline, Gemini integratsiya
- **B (data):** bilim bazasini to'ldirish va TEKSHIRISH (eng muhim rol!)
- **C (product):** bot UX (menyu, tugmalar), test ssenariylar, demo/prezentatsiya

2 kishi bo'lsa: A = backend + product, B = data + test.

---

## 4. Haftalik ish reja

### 1-hafta — Ma'lumot va skelet (eng muhim hafta)

**Data (B):**
- `bilim_bazasi.json` dagi 10 ta tayyor yozuvni tekshirish: har bir telefon raqami, portal manzili, idora nomini **rasmiy manbadan** (my.gov.uz, lex.uz, idoraning o'z sayti) tasdiqlash. Tasdiqlanmagan yozuv bazaga kirmaydi.
- Yana 20 ta eng ko'p uchraydigan muammoni yig'ish. Manbalar: my.gov.uz xizmatlar katalogi, pm.gov.uz statistikasi (qaysi mavzuda ko'p murojaat bo'ladi), tanish-bilishlardan so'rov.
- Har yozuvga `manba` maydonini majburiy to'ldirish.

**Backend (A):**
- BotFather'dan bot token, ai.google.dev dan API kalit olish.
- "Hello world" bot: /start → salomlashish → istalgan matnga echo.
- Gemini API'ga birinchi so'rov ishlashini tekshirish.

**Natija:** 30 ta tasdiqlangan yozuv + ishlaydigan bo'sh bot.

### 2-hafta — RAG yadro

- JSON yozuvlarni ChromaDB'ga yuklash skripti (`index_qurish.py`): har yozuvdan qidiruv matni yasash (muammo + kalit so'zlar), embedding olish, saqlash.
- Qidiruv funksiyasi: savol → top-3 yozuv.
- System prompt yozish (loyihaning "yuragi"):
  - faqat berilgan yozuvlarga tayanish;
  - yozuv mos kelmasa — ochiq aytish;
  - javob strukturasi: 1) mas'ul idora 2) murojaat kanali 3) kerakli hujjatlar 4) tartib 5) manba;
  - huquqiy maslahat bermaslik, faqat yo'naltirish.
- 20 ta test-savol bilan sifatni tekshirish (shu jumladan kirillcha va xato yozilgan savollar).

**Natija:** savol berilsa to'g'ri idorani manba bilan aytadigan bot.

### 3-hafta — UX va mustahkamlik

- /start onboarding: bot nima qila oladi, nima qila olmaydi (2–3 jumla).
- Kategoriya tugmalari (inline keyboard): Kommunal / Mehnat / Ijtimoiy / Yer-mulk / Tadbirkorlik / Boshqa — yozishni bilmaganlar uchun.
- Javob oxirida: "Foydali bo'ldimi? 👍/👎" (oddiy feedback log — himoyada ko'rsatish uchun metrika).
- Xatolarni ushlash: Gemini limitga urilsa — "birozdan keyin urinib ko'ring"; bo'sh natija — fallback javob.
- Kirill ↔ lotin: har ikkala yozuvni sinash (Gemini odatda o'zi eplaydi, lekin tekshirish shart).
- Bazani 40–50 yozuvga yetkazish.

**Natija:** begona odam ishlata oladigan bot.

### 4-hafta — Sayqal, demo, (ixtiyoriy) web

- 10–15 kishiga botni berib real test, feedback bo'yicha tuzatish.
- Demo ssenariy tayyorlash: 3 ta jonli misol (masalan: elektr uzilishi, ish haqi, kadastr) — har birida bot javobi + manba ko'rinadi.
- Prezentatsiya: muammo → yechim → arxitektura → jonli demo → metrikalar (nechta yozuv, feedback %) → keyingi rejalar (Yashil Makon moduli!).
- **Ixtiyoriy bonus:** bitta sahifali web-landing (oddiy HTML): loyiha tavsifi + botga link + skrinshotlar. Vaqt qolsa — web-chat ham, lekin bu shart emas.

**Natija:** himoyaga tayyor MVP.

---

## 5. Xavflar va yechimlar

| Xavf | Yechim |
|---|---|
| Bot noto'g'ri idora aytadi | Faqat RAG'dan javob + har javobda manba + "yo'naltiruvchi, huquqiy maslahat emas" disclaimer |
| Gemini bepul limiti tugaydi | Kunlik limit MVP uchun yetarli; zaxira: Groq API (bepul) |
| Ma'lumot eskiradi (idora nomi o'zgaradi) | Har yozuvda `tekshirilgan_sana` maydoni; oyiga bir yangilash |
| O'zbekcha xato yozilgan savollar | Kalit so'zlarga xato variantlarni ham qo'shish; embedding semantik qidiradi — bu yordam beradi |
| Vaqt yetmasligi | Kesish tartibi: avval web bonus, keyin feedback tugmalari, keyin kategoriya menyusi. RAG yadro va data — hech qachon kesilmaydi |

---

## 6. Muvaffaqiyat mezonlari (himoya uchun)

- ≥ 40 ta tasdiqlangan yozuv bazada
- Test-savollarning ≥ 80% ida to'g'ri idora aytiladi
- Bazada yo'q savollarda bot to'qib chiqarmaydi (10 ta "tuzoq" savol bilan tekshiriladi)
- ≥ 10 real foydalanuvchi sinagan
