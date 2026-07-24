# Indekslash skripti: data/ papkasidagi barcha bazalar → ChromaDB
# Ishga tushirish:  python -m bot.index_qurish

import json
import time

from bot.config import BILIM_BAZASI_YOLI, MY_GOV_YOLI, PM_GOV_YOLI, LEX_YOLI, SAVOL_JAVOB_YOLI
from bot.rag import embed, collection, TokenlarTugadi


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

# Portal bazalari bir xil sxemada (xizmatlar ro'yxati): fayl yo'li va id-prefiks.
# Prefiks turli bazalardagi id to'qnashuvining oldini oladi.
PORTAL_BAZALARI = [
    (MY_GOV_YOLI, "mygov-", "my-gov"),
    (PM_GOV_YOLI, "pmgov-", "pm-gov"),
    (LEX_YOLI, "lex-", "lex"),
    (SAVOL_JAVOB_YOLI, "advice-", "savol-javob"),
]


def bazani_yuklash():
    """data/ papkasidagi barcha bazalarni ChromaDB ga indekslaydi:
    1) bilim_bazasi.json — muammo → idora yozuvlari;
    2) portal bazalari (my-gov, pm-gov, lex) — xizmatlar URL va
       qadam-baqadam yo'riqnomalar bilan."""
    with open(BILIM_BAZASI_YOLI, encoding="utf-8") as f:
        data = json.load(f)

    yozuvlar = [y for y in data["yozuvlar"]]  # MVP test uchun hammasi;
    # ishga chiqarishda: [y for y in data["yozuvlar"] if y["tekshirilgan"]]

    for y in yozuvlar:
        qidiruv_matni = y["muammo"] + " " + " ".join(y["kalit_sozlar"])
        emb = _embed_sabr_bilan(qidiruv_matni)
        collection.upsert(
            ids=[y["id"]],
            embeddings=[emb],
            documents=[json.dumps(y, ensure_ascii=False)],
        )
    print(f"bilim_bazasi: {len(yozuvlar)} ta yozuv indekslandi.")

    for yol, prefiks, nom in PORTAL_BAZALARI:
        if not yol.exists():
            print(f"{nom}: fayl topilmadi, o'tkazib yuborildi.")
            continue
        with open(yol, encoding="utf-8") as f:
            baza = json.load(f)

        xizmatlar = baza["xizmatlar"]
        for x in xizmatlar:
            # ikki tur yozuv: xizmat (xizmat_nomi+tavsif) yoki savol-javob (savol+qisqa_javob)
            nomi = x.get("xizmat_nomi") or x.get("savol", "")
            tavsifi = x.get("tavsif") or x.get("qisqa_javob", "")
            qidiruv_matni = nomi + " " + " ".join(x["muammolar"]) + " " + tavsifi
            emb = _embed_sabr_bilan(qidiruv_matni)
            collection.upsert(
                ids=[prefiks + x["id"]],
                embeddings=[emb],
                documents=[json.dumps(x, ensure_ascii=False)],
            )
        print(f"{nom}: {len(xizmatlar)} ta xizmat indekslandi.")


if __name__ == "__main__":
    bazani_yuklash()
