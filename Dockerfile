# Compass backend (FastAPI) — Render uchun konteyner.
#
# Frontend bu obrazga kirmaydi: u Netlify'da turadi va `/api/*` ni shu servisga
# proksilaydi. Ma'lumotlar Supabase Postgres'da, shuning uchun saqlanadigan
# disk ham kerak emas.
#
# Yig'ish va yuborish (repo ildizidan):
#     docker build -t ghcr.io/umarkhn1/compass-api:latest .
#     docker push ghcr.io/umarkhn1/compass-api:latest
# So'ng Render'da servisni qayta deploy qiling (yangi obrazni tortib oladi):
#     curl -X POST https://api.render.com/v1/services/srv-d9qskh9t0dsc738l7mj0/deploys \
#          -H "Authorization: Bearer $RENDER_TOKEN" -H "Content-Type: application/json" -d '{}'
#
# Obraz xususiy (ichida manba kodi bor) — Render uni registry credentials
# orqali tortadi (ghcr-umarkhn1).

FROM python:3.12-slim

# Python: .pyc yozmasin, log'lar buferlanmasin (Render jurnalida darhol ko'rinadi).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Avval faqat requirements — kod o'zgarganda bog'liqliklar qayta o'rnatilmaydi.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render $PORT ni o'zi beradi; mahalliy ishga tushirishda 8000 bo'ladi.
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn web.main:app --host 0.0.0.0 --port ${PORT}"]
