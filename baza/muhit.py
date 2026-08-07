"""`.env` faylini environment'ga yuklash — bot, web va baza uchun umumiy.

Export qilingan o'zgaruvchilar ustun turadi (`setdefault`), shuning uchun
serverda `.env` faylsiz, faqat environment orqali ham ishlatish mumkin.
"""

from __future__ import annotations

import os
from pathlib import Path

LOYIHA_ILDIZI = Path(__file__).resolve().parent.parent
ENV_FAYLI = LOYIHA_ILDIZI / ".env"

_yuklandi = False


def env_yuklash(yol: Path | None = None) -> None:
    """`.env` ni bir marta o'qib, topilgan qiymatlarni `os.environ` ga qo'yadi."""
    global _yuklandi
    if _yuklandi and yol is None:
        return
    _yuklandi = True

    fayl = yol or ENV_FAYLI
    if not fayl.is_file():
        return

    for qator in fayl.read_text(encoding="utf-8").splitlines():
        qator = qator.strip()
        if not qator or qator.startswith("#") or "=" not in qator:
            continue
        nom, _, qiymat = qator.partition("=")
        os.environ.setdefault(nom.strip(), qiymat.strip().strip("'\""))
