# Cloudflare — domen va frontend sozlamalari

Frontend (React SPA) Cloudflare Workers'da, backend (API + bot) — sizning
serveringizda (`docker-compose.yml`, batafsil: [DEPLOY.md](DEPLOY.md)).
Ikkalasi bitta domenda (`yonaltiruvchi.uz`) ishlaydi: Worker statikani o'zi
beradi, `/api/*` va `/ws/*` so'rovlarini esa serveringizga proksilaydi
(`web/frontend/worker.js`). Shu tufayli CORS, cookie sozlamalari va frontend
kodida hech narsa o'zgartirish shart emas.

## 0. Talab qilinadigan ma'lumotlar

- Cloudflare akkaunt (bepul reja yetadi)
- `yonaltiruvchi.uz` domeni Cloudflare'ga ulangan (nameserver'lar Cloudflare'ga
  ko'chirilgan — agar hali qilinmagan bo'lsa: Cloudflare Dashboard → **Add a
  site** → domenni kiriting → ko'rsatilgan nameserver'larni domen
  registratoringizda (masalan REG.UZ) o'rnating; DNS tarqalishi bir necha
  soatgacha davom etishi mumkin)
- Serveringizning ochiq IP manzili (docker-compose bilan backend shu yerda
  ishlaydi)

## 1. DNS: backend uchun "yashirin" origin yozuvi

Worker `/api` va `/ws` so'rovlarini `origin.yonaltiruvchi.uz` manziliga
yuboradi (`worker.js`dagi `BACKEND_ORIGIN`) — bu ochiq saytning manzili emas,
faqat Worker bilan Caddy o'rtasidagi ichki ulanish uchun.

Cloudflare Dashboard → **yonaltiruvchi.uz** → **DNS** → **Add record**:

| Type | Name | Content | Proxy status |
|---|---|---|---|
| A | `origin` | serveringiz IP manzili | **DNS only** (kulrang bulut — sariq emas!) |

⚠️ Proxy status albatta **DNS only** bo'lishi kerak: Caddy shu hostga
Let's Encrypt sertifikatini to'g'ridan-to'g'ri oladi, Cloudflare'ning proksisi
orasida tursa buning uchun HTTP-01 tekshiruvi va Worker'ning to'g'ridan-to'g'ri
ulanishi murakkablashadi.

## 2. Worker'ni deploy qilish

Lokal mashinada (yoki serverda, Node.js 20+ bo'lsa):

```bash
cd web/frontend
npm install
npx wrangler login        # brauzer orqali Cloudflare akkauntga kirish, bir marta
npm run deploy             # build + wrangler deploy
```

Birinchi `wrangler deploy`dan keyin Cloudflare Workers'da `compass-web`
nomli loyiha paydo bo'ladi (`*.workers.dev` manzilida sinab ko'rish mumkin,
lekin bizga custom domain kerak — keyingi qadam).

## 3. Custom domain: yonaltiruvchi.uz → Worker

Cloudflare Dashboard → **Workers & Pages** → **compass-web** → **Settings** →
**Domains & Routes** → **Add** → **Custom Domain**:

- `yonaltiruvchi.uz` qo'shing — Cloudflare kerakli DNS yozuvini va
  sertifikatni **o'zi avtomatik** yaratadi.

## 4. www.yonaltiruvchi.uz → yonaltiruvchi.uz (redirect)

Alohida Worker domain qo'shish shart emas — oddiy redirect qoidasi yetarli:

Cloudflare Dashboard → **yonaltiruvchi.uz** → **Rules** → **Redirect Rules**
→ **Create rule**:

- **Rule name**: `www → root`
- **If incoming requests match**: Hostname → equals → `www.yonaltiruvchi.uz`
- **Then**: Dynamic redirect → `concat("https://yonaltiruvchi.uz", http.request.uri.path)`
- **Status code**: 301
- Save and Deploy

Bu qoida ishlashi uchun `www.yonaltiruvchi.uz` uchun ham DNS yozuvi kerak —
**DNS** bo'limida `CNAME www → yonaltiruvchi.uz`, Proxy status: **Proxied**
(sariq bulut), qo'shing.

## 5. Kesh: katalog so'rovlari uchun Cache Rule

`/api/sohalar`, `/api/xizmatlar`, `/api/manbalar`, `/api/savol-javob`,
`/api/statistika` — bularning ma'lumoti kamdan-kam o'zgaradi, shuning uchun
Cloudflare edge'da keshlash mantiqan: birinchi so'rovdan keyin butun dunyo
bo'ylab foydalanuvchilar serveringizga umuman tegmasdan javob oladi.

Cloudflare Dashboard → **yonaltiruvchi.uz** → **Caching** → **Cache Rules**
→ **Create rule**:

- **Rule name**: `Katalog API keshi`
- **If incoming requests match** → Custom filter expression:
  ```
  (http.request.uri.path in {"/api/sohalar" "/api/xizmatlar" "/api/manbalar" "/api/savol-javob" "/api/statistika"}) and (http.request.method eq "GET")
  ```
- **Then**: Cache eligibility → **Eligible for cache**
- **Edge TTL** → Ignore cache-control header and use this TTL → **1 hour**
  (yoki kerakli muddat — katalog necha vaqtda o'zgarishiga qarab)
- Save and Deploy

⚠️ `/api/savol` (chat) va `/api/auth/*` bu ro'yxatga **kiritilmasin** — ular
shaxsiy/dinamik, keshlash noto'g'ri javob berib qo'yishi mumkin.

Yangi ma'lumot chiqarganingizda (masalan `data/*.json`ni yangilab qayta
deploy qilganingizda) eski kesh 1 soatgacha turishi mumkin — kerak bo'lsa
**Caching** → **Configuration** → **Purge Cache** → **Custom Purge** bilan
tezlashtirish mumkin.

## 6. Tekshirish

```bash
curl -I https://yonaltiruvchi.uz/                      # frontend, Cloudflare'dan
curl -I https://www.yonaltiruvchi.uz/                  # 301 → yonaltiruvchi.uz
curl https://yonaltiruvchi.uz/api/sohalar               # Worker orqali backendga proksilangan
```

Sayt to'liq ishlayotgan bo'lishi kerak: kategoriyalar, chat, kirish/ro'yxat,
soat (`/ws/vaqt`) — hammasi bitta domenda.

## Keyingi deploylar

Frontend o'zgarganda:

```bash
cd web/frontend && npm run deploy
```

Backend o'zgarganda — [DEPLOY.md](DEPLOY.md)dagi `git pull && docker compose
up -d --build` serverda.

## Nima uchun bitta domen (subdomain emas)

`api.yonaltiruvchi.uz` kabi alohida subdomen o'rniga Worker o'zi proksi
qilishi tanlandi — shu tufayli CORS sozlash, cookie'ni `SameSite=None`ga
o'zgartirish va frontend kodidagi barcha `/api` so'rovlarini to'liq URL'ga
almashtirish shart bo'lmadi (`web/frontend/src/shared/api/httpClient.ts` va
`useServerClock.ts` nisbiy manzillardan foydalanadi — ular o'zgarishsiz
ishlayveradi).
