"""assets/images/*.png → web/frontend/public/images/*.png

Logotip fayllarida "compass" yozuvi ham bor, saytda esa nom alohida matn bilan
yoziladi. Shu skript yozuvni kesib tashlab, faqat belgini (mark) tayyorlaydi:

    light-logo.png → logo-mark-light.png   (yorug' mavzu uchun, rangli)
    dark-logo.png  → logo-mark-dark.png    (qorong'i mavzu uchun, oq chizmali)
    ai-logo.png    → ai-logo.png           (chat tugmasi; kesilmaydi, faqat ko'chiriladi)

Logotip almashtirilganda shu buyruqni qayta ishga tushiring:

    python -m web.eksport_logo
"""

import shutil

from PIL import Image

from web.config import FRONTEND_YOLI, LOYIHA_ILDIZI

MANBA = LOYIHA_ILDIZI / "assets" / "images"
NATIJA = FRONTEND_YOLI / "public" / "images"

# Belgi ostidagi yozuvni kesib tashlanadigan fayllar.
KESILADIGANLAR = {
    "light-logo.png": ("logo-mark-light.png", False),  # oq fon (shaffof emas)
    "dark-logo.png": ("logo-mark-dark.png", True),  # shaffof fon
}
# O'zgarishsiz ko'chiriladiganlar.
KOCHIRILADIGANLAR = ("ai-logo.png", "light-logo.png", "dark-logo.png")

TOMON = 512  # natija o'lchami


def _bandlar(qatorlar: list[bool]) -> list[tuple[int, int]]:
    """Ketma-ket "siyoh bor" qatorlarni guruhlarga ajratadi."""
    natija: list[tuple[int, int]] = []
    joriy: list[int] | None = None
    for y, bor in enumerate(qatorlar):
        if bor:
            joriy = [y, y] if joriy is None else [joriy[0], y]
        elif joriy is not None:
            natija.append((joriy[0], joriy[1]))
            joriy = None
    if joriy is not None:
        natija.append((joriy[0], joriy[1]))
    return natija


def belgini_kesish(kirish, chiqish, shaffof_fon: bool) -> None:
    im = Image.open(kirish).convert("RGBA")
    w, h = im.size
    px = im.load()

    def siyohmi(x: int, y: int) -> bool:
        r, g, b, a = px[x, y]
        if shaffof_fon:
            return a > 30
        return a > 30 and (255 - min(r, g, b)) > 35  # oq fondan farq qiladimi

    qatorlar = [any(siyohmi(x, y) for x in range(0, w, 3)) for y in range(h)]
    guruhlar = [g for g in _bandlar(qatorlar) if g[1] - g[0] > h * 0.02]
    if len(guruhlar) < 2:
        raise SystemExit(f"{kirish.name}: belgi va yozuv ajratilmadi ({guruhlar})")

    # Oxirgi guruh — "compass" yozuvi, uni tashlab yuboramiz.
    y1, y2 = guruhlar[0][0], guruhlar[-2][1]
    ustunlar = [any(siyohmi(x, y) for y in range(y1, y2, 3)) for x in range(w)]
    x1 = next(i for i, v in enumerate(ustunlar) if v)
    x2 = w - 1 - next(i for i, v in enumerate(reversed(ustunlar)) if v)

    chek = int(max(x2 - x1, y2 - y1) * 0.04)
    kesilgan = im.crop(
        (max(x1 - chek, 0), max(y1 - chek, 0), min(x2 + chek, w), min(y2 + chek, h))
    )

    # Kvadratga tekislaymiz — interfeysda o'lcham har doim bir xil bo'lsin.
    tomon = max(kesilgan.size)
    fon = Image.new("RGBA", (tomon, tomon), (0, 0, 0, 0))
    fon.paste(kesilgan, ((tomon - kesilgan.width) // 2, (tomon - kesilgan.height) // 2))
    fon.thumbnail((TOMON, TOMON), Image.LANCZOS)
    fon.save(chiqish)
    print(f"  {kirish.name} → {chiqish.name} {fon.size}")


def main() -> None:
    NATIJA.mkdir(parents=True, exist_ok=True)

    for nom in KOCHIRILADIGANLAR:
        manba = MANBA / nom
        if manba.is_file():
            shutil.copy2(manba, NATIJA / nom)
            print(f"  {nom} ko'chirildi")

    for nom, (chiqish_nomi, shaffof) in KESILADIGANLAR.items():
        manba = MANBA / nom
        if not manba.is_file():
            print(f"  {nom} topilmadi — o'tkazib yuborildi")
            continue
        belgini_kesish(manba, NATIJA / chiqish_nomi, shaffof)


if __name__ == "__main__":
    main()
