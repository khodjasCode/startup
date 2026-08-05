"""data/*.json → web/frontend/public/data/katalog.json

Frontend odatda `/api/...` orqali ishlaydi, lekin backend ishga tushirilmagan
bo'lsa (masalan faqat `npm run dev` bilan dizayn ustida ishlanayotganda) shu
eksport faylidan o'qiydi — sayt baribir haqiqiy ma'lumot bilan to'ladi.

Ishga tushirish (repo ildizidan, hech qanday API kalit kerak emas):
    python -m web.eksport_katalog

`npm run build` va `npm run dev` buni avtomatik chaqiradi (package.json).
"""

import json

from web.config import KATALOG_EKSPORT_YOLI
from web.xizmat import katalog_bazasi as baza


def eksport() -> dict:
    xizmatlar = baza.barcha_xizmatlar()
    return {
        "sohalar": baza.sohalar(),
        "manbalar": [m.dict() for m in baza.barcha_manbalar()],
        "statistika": {
            kalit: qiymat for kalit, qiymat in baza.statistika().items() if kalit != "manbalar"
        },
        # Bitta ro'yxat: frontend uni o'zi filtrlaydi (soha, matn, sahifalash).
        "xizmatlar": [x.toliq() for x in xizmatlar],
    }


def main() -> None:
    natija = eksport()
    KATALOG_EKSPORT_YOLI.parent.mkdir(parents=True, exist_ok=True)
    KATALOG_EKSPORT_YOLI.write_text(
        json.dumps(natija, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    olcham = KATALOG_EKSPORT_YOLI.stat().st_size / 1024
    print(
        f"{KATALOG_EKSPORT_YOLI.relative_to(KATALOG_EKSPORT_YOLI.parents[4])}: "
        f"{len(natija['xizmatlar'])} yozuv, {olcham:.0f} KB"
    )


if __name__ == "__main__":
    main()
