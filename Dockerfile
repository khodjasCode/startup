# Backend: FastAPI + bot yadrosi (Telegram bot va web API).
#
# Frontend endi shu image ichida QURILMAYDI — u alohida Cloudflare Workers'ga
# deploy qilinadi (web/frontend/wrangler.toml). Bu konteyner faqat API'ni
# beradi, uni Cloudflare Worker /api va /ws yo'llari uchun proksilaydi
# (batafsil: CLOUDFLARE.md).
FROM python:3.12-slim
WORKDIR /app
# docker/index_init.py skript sifatida ishga tushadi (`python docker/index_init.py`),
# shu holatda Python faqat skript papkasini sys.path'ga qo'shadi — /app'dagi
# bot/web paketlarini topolmay qoladi. PYTHONPATH bilan buni tuzatamiz.
ENV PYTHONPATH=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot ./bot
COPY web ./web
COPY data ./data
COPY docker/index_init.py ./docker/index_init.py

EXPOSE 8000
CMD ["uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8000"]
