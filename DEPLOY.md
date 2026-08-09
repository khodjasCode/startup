# Deploy — yonaltiruvchi.uz

Arxitektura ikkiga bo'lingan:

- **Frontend** (React SPA) — Cloudflare Workers'da. Sozlash: [CLOUDFLARE.md](CLOUDFLARE.md).
- **Backend** (API + Telegram-bot) — shu faylda tasvirlangan, sizning
  serveringizda, `docker-compose.yml` orqali. Serverda faqat Docker kerak —
  Python, Node.js yoki ChromaDB'ni qo'lda o'rnatish shart emas.

Ikkalasi bitta domenda (`yonaltiruvchi.uz`) ishlaydi: Cloudflare Worker
statik frontendni o'zi beradi, `/api` va `/ws` so'rovlarini esa shu yerdagi
serverga proksilaydi. Server ochiq internetga **frontend orqali emas**,
faqat `origin.yonaltiruvchi.uz` degan ichki nom orqali ko'rinadi — shuning
uchun backend Docker image'ida frontend build umuman yo'q (u Cloudflare'da).

Server yengil bo'lishi uchun: har bir konteynerga xotira/CPU chegarasi va
log-rotatsiya qo'yilgan (`docker-compose.yml`dagi `mem_limit`/`x-log`) — disk
loglardan asta-sekin to'lib qolmaydi, birorta jarayon xotirani "yeb
qo'ymaydi". Amalda `web`/`bot` process'lari ~35–110 MB atrofida ishlaydi
(mahalliy sinovda o'lchandi); `mem_limit: 400m` shunga nisbatan katta zaxira.

## Nima ishga tushadi

| Xizmat | Vazifasi |
|---|---|
| `index-init` | Bir marta ishga tushib, bilim bazasini ChromaDB'ga indekslaydi, so'ng to'xtaydi (`vektor_baza` volume'da saqlanadi — qayta ishga tushirilsa qayta indekslamaydi) |
| `web` | FastAPI — faqat `/api`, `/ws` (frontend endi shu image'da yo'q), `index-init` tugagach ishga tushadi |
| `bot` | Telegram-bot (long polling), `index-init` tugagach ishga tushadi |
| `caddy` | 80/443-portlarni oladi, `origin.yonaltiruvchi.uz` uchun Let's Encrypt sertifikatini **avtomatik** oladi va yangilaydi, `web`ga proksilaydi |

## 1. Serverda bir martalik tayyorgarlik

```bash
# Docker + Compose plugin (Ubuntu/Debian misolida)
curl -fsSL https://get.docker.com | sh

# Firewall: 80 va 443 ochiq bo'lishi kerak (Let's Encrypt shu orqali tekshiradi)
sudo ufw allow 80,443/tcp   # yoki serveringiz provayderi paneli orqali
```

DNS: `origin.yonaltiruvchi.uz` (A-yozuv, **DNS only** — kulrang bulut) shu
server IP manziliga ko'rsatilgan bo'lishi kerak — aks holda Caddy sertifikat
ololmaydi. Bu yozuvni qanday qo'shish: [CLOUDFLARE.md](CLOUDFLARE.md) 1-qadam.

## 2. Repo va kalitlar

```bash
git clone <repo-url> compass && cd compass
cp .env.example .env
nano .env   # BOT_TOKEN, GEMINI_API_KEY, kerak bo'lsa GEMINI_API_KEY_ZAXIRA,
            # CADDY_EMAIL (Let's Encrypt bildirishnomalari uchun)
```

`.env` git'ga tushmaydi (`.gitignore`da) — kalitlar faqat serverda qoladi.

## 3. Ishga tushirish

```bash
docker compose up -d --build
```

Birinchi marta `index-init` bilim bazasini (300+ yozuv) Gemini orqali
indekslaydi — bir necha daqiqa ketishi mumkin. Kuzatish:

```bash
docker compose logs -f index-init
```

Tugagach `web` va `bot` avtomatik ishga tushadi, Caddy esa sertifikatni oladi:

```bash
docker compose ps
docker compose logs -f caddy   # "certificate obtained successfully" kutiladi
```

Backend tayyor: `https://origin.yonaltiruvchi.uz` (faqat `/api`, `/ws` —
brauzerda ochilmaydi, chunki frontend yo'q). Ochiq sayt — Cloudflare
qadamlaridan keyin **https://yonaltiruvchi.uz** da.

## 4. Yangilash (keyingi deploylar)

```bash
git pull
docker compose up -d --build
```

`vektor_baza` va `foydalanuvchilar.json` (foydalanuvchi hisoblari) alohida
Docker volume'larda saqlanadi — qayta build/deploy qilinganda yo'qolmaydi.

Frontend o'zgarganda — server bilan aloqasi yo'q, alohida:
[CLOUDFLARE.md](CLOUDFLARE.md) → "Keyingi deploylar".

## 5. Foydali buyruqlar

```bash
docker compose logs -f web       # web/API loglari
docker compose logs -f bot       # Telegram-bot loglari
docker compose restart bot       # faqat botni qayta ishga tushirish
docker compose down              # hammasini to'xtatish (volume'lar saqlanadi)
docker stats                     # real vaqtda xotira/CPU sarfini ko'rish
```

## Eslatma

- Bir nechta server nusxasi (masalan load balancer orqasida) uchun mos emas —
  `foydalanuvchilar.json` va suhbat tarixi (xotirada) bitta nusxa uchun
  mo'ljallangan (`instructions/WEB.md`dagi eslatma bilan bir xil).
- Domenni o'zgartirish kerak bo'lsa — `Caddyfile` va
  `web/frontend/wrangler.toml`dagi `BACKEND_ORIGIN`ni yangilang.
- Server juda kuchsiz (masalan 512 MB RAM) bo'lsa — `docker-compose.yml`dagi
  `mem_limit` qiymatlarini pasaytiring, lekin 300m dan pastga tushirmang
  (ChromaDB + Gemini SDK import qilinganda ~110 MB'gacha ko'tarilishi mumkin).
