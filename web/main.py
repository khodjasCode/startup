# Compass web serveri: API (chat, katalog, avtorizatsiya, fikr) + React frontend.
#
# Ishga tushirish (repo root'dan):
#   cd web/frontend && npm install && npm run build   # bir marta / frontend o'zgarganda
#   uvicorn web.main:app --reload                     # http://127.0.0.1:8000
#
# Frontendni ishlab chiqish rejimida:
#   uvicorn web.main:app --reload      (API — 8000-portda)
#   cd web/frontend && npm run dev     (UI — 5173-portda, /api 8000 ga proksilanadi)

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from web.api import auth, chat, katalog, vaqt
from web.config import FRONTEND_DIST_YOLI as FRONTEND_YOLI

INDEX_FAYLI = FRONTEND_YOLI / "index.html"

YIGILMAGAN_XABAR = """
<!doctype html><meta charset="utf-8">
<title>Compass — frontend yig'ilmagan</title>
<body style="font-family: system-ui; max-width: 40rem; margin: 4rem auto; line-height: 1.6">
<h1>Frontend hali yig'ilmagan</h1>
<p><code>web/frontend/dist</code> topilmadi. Repo ildizida quyidagini bajaring:</p>
<pre style="background:#f4f4f5; padding:12px; border-radius:8px">cd web/frontend
npm install
npm run build</pre>
<p>Ishlab chiqish rejimida esa <code>npm run dev</code> (5173-port) ishlatiladi —
u <code>/api</code> so'rovlarini shu serverga proksilaydi.</p>
</body>
"""

app = FastAPI(title="Compass web")

app.include_router(chat.router)
app.include_router(katalog.router)
app.include_router(auth.router)
app.include_router(vaqt.router)

# Vite hashli fayl nomlaridan foydalanadi (index-a1b2c3.js), shuning uchun
# /assets uzoq muddat keshlanishi mumkin; index.html esa keshlanmaydi.
for _papka in ("assets", "images", "data"):
    _yol = FRONTEND_YOLI / _papka
    if _yol.is_dir():
        app.mount(f"/{_papka}", StaticFiles(directory=_yol), name=_papka)


# SPA fallback — API marshrutlaridan KEYIN e'lon qilinadi, ular ustun turishi uchun.
@app.get("/{yol:path}")
async def spa(yol: str):
    """Barcha noma'lum yo'llar index.html ga qaytariladi (client-side routing)."""
    del yol
    if not INDEX_FAYLI.is_file():
        return HTMLResponse(YIGILMAGAN_XABAR, status_code=503)
    return FileResponse(INDEX_FAYLI, headers={"Cache-Control": "no-cache"})
