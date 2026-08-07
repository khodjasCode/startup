# Indekslash skripti: data/ papkasidagi barcha bazalar → PostgreSQL (pgvector)
# Ishga tushirish:  python3 -m bot.index_qurish
#
# Har bir yozuv uchun Gemini'dan embedding olinadi va `vektorlar` jadvaliga
# yoziladi. Qayta ishga tushirish xavfsiz: yozuvlar id bo'yicha yangilanadi.
# `--yangilarini` bilan faqat bazada yo'q yozuvlar indekslanadi (uzilib qolgan
# indekslashni davom ettirish uchun — allaqachon olingan embedding'lar uchun
# qayta to'lanmaydi).

import json
import sys
import time

import baza
from bot.config import BILIM_BAZASI_YOLI, MY_GOV_YOLI, PM_GOV_YOLI, LEX_YOLI, SAVOL_JAVOB_YOLI
from bot.rag import embed, vektor_matni, vektorlar_soni, TokenlarTugadi


def _embed_sabr_bilan(matn: str, urinishlar: int = 10):
    """Katta bazani indekslashda barcha kalitlar limitga urilsa, 30 soniya
    kutib qayta urinadi — indekslash o'rtada uzilib qolmasligi uchun."""
    for _ in range(urinishlar):
        try:
            return embed(matn)
        except TokenlarTugadi:
            print("    ... limit (429), 30 soniya kutilmoqda")
            time.sleep(30)
    raise TokenlarTugadi()


def _saqlash(yozuv_id: str, manba: str, hujjat: str, emb: list[float]) -> None:
    baza.bajarish(
        "insert into vektorlar (id, manba, hujjat, embedding) values (%s, %s, %s, %s::vector) "
        "on conflict (id) do update set manba = excluded.manba, hujjat = excluded.hujjat, "
        "embedding = excluded.embedding, yangilangan = now()",
        (yozuv_id, manba, hujjat, vektor_matni(emb)),
    )


def _mavjud_idlar() -> set[str]:
    return {q["id"] for q in baza.sorov("select id from vektorlar")}


# Portal bazalari bir xil sxemada (xizmatlar ro'yxati): fayl yo'li va id-prefiks.
# Prefiks turli bazalardagi id to'qnashuvining oldini oladi.
PORTAL_BAZALARI = [
    (MY_GOV_YOLI, "mygov-", "my-gov"),
    (PM_GOV_YOLI, "pmgov-", "pm-gov"),
    (LEX_YOLI, "lex-", "lex"),
    (SAVOL_JAVOB_YOLI, "advice-", "savol-javob"),
]


def bazani_yuklash(faqat_yangilari: bool = False):
    """data/ papkasidagi barcha bazalarni `vektorlar` jadvaliga indekslaydi:
    1) bilim_bazasi.json — muammo → idora yozuvlari;
    2) portal bazalari (my-gov, pm-gov, lex) — xizmatlar URL va
       qadam-baqadam yo'riqnomalar bilan."""
    baza.sxemani_yaratish()
    mavjud = _mavjud_idlar() if faqat_yangilari else set()

    with open(BILIM_BAZASI_YOLI, encoding="utf-8") as f:
        data = json.load(f)

    yozuvlar = [y for y in data["yozuvlar"]]  # MVP test uchun hammasi;
    # ishga chiqarishda: [y for y in data["yozuvlar"] if y["tekshirilgan"]]

    yangi = 0
    for y in yozuvlar:
        if y["id"] in mavjud:
            continue
        qidiruv_matni = y["muammo"] + " " + " ".join(y["kalit_sozlar"])
        emb = _embed_sabr_bilan(qidiruv_matni)
        _saqlash(y["id"], "bilim-bazasi", json.dumps(y, ensure_ascii=False), emb)
        yangi += 1
    print(f"bilim_bazasi: {yangi}/{len(yozuvlar)} ta yozuv indekslandi.", flush=True)

    for yol, prefiks, nom in PORTAL_BAZALARI:
        if not yol.exists():
            print(f"{nom}: fayl topilmadi, o'tkazib yuborildi.")
            continue
        with open(yol, encoding="utf-8") as f:
            manba_bazasi = json.load(f)

        xizmatlar = manba_bazasi["xizmatlar"]
        yangi = 0
        for x in xizmatlar:
            yozuv_id = prefiks + x["id"]
            if yozuv_id in mavjud:
                continue
            # ikki tur yozuv: xizmat (xizmat_nomi+tavsif) yoki savol-javob (savol+qisqa_javob)
            nomi = x.get("xizmat_nomi") or x.get("savol", "")
            tavsifi = x.get("tavsif") or x.get("qisqa_javob", "")
            qidiruv_matni = nomi + " " + " ".join(x["muammolar"]) + " " + tavsifi
            emb = _embed_sabr_bilan(qidiruv_matni)
            _saqlash(yozuv_id, nom, json.dumps(x, ensure_ascii=False), emb)
            yangi += 1
        print(f"{nom}: {yangi}/{len(xizmatlar)} ta xizmat indekslandi.", flush=True)

    print(f"Jami indeksda: {vektorlar_soni()} ta yozuv.")


if __name__ == "__main__":
    bazani_yuklash(faqat_yangilari="--yangilarini" in sys.argv[1:])
