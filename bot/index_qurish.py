# Indekslash skripti: bilim_bazasi.json + my-gov.json → ChromaDB
# Ishga tushirish:  python -m bot.index_qurish

import json

from bot.config import BILIM_BAZASI_YOLI, MY_GOV_YOLI
from bot.rag import embed, collection


def bazani_yuklash():
    """data/ papkasidagi ikkala bazani ChromaDB ga indekslaydi:
    1) bilim_bazasi.json — muammo → idora yozuvlari;
    2) my-gov.json — my.gov.uz portal xizmatlari (URL va qadam-baqadam
       yo'riqnomalar bilan). Id to'qnashuvi bo'lmasligi uchun bu yozuvlar
       "mygov-" prefiksi bilan saqlanadi."""
    with open(BILIM_BAZASI_YOLI, encoding="utf-8") as f:
        data = json.load(f)

    yozuvlar = [y for y in data["yozuvlar"]]  # MVP test uchun hammasi;
    # ishga chiqarishda: [y for y in data["yozuvlar"] if y["tekshirilgan"]]

    for y in yozuvlar:
        qidiruv_matni = y["muammo"] + " " + " ".join(y["kalit_sozlar"])
        emb = embed(qidiruv_matni)
        collection.upsert(
            ids=[y["id"]],
            embeddings=[emb],
            documents=[json.dumps(y, ensure_ascii=False)],
        )
    print(f"bilim_bazasi: {len(yozuvlar)} ta yozuv indekslandi.")

    with open(MY_GOV_YOLI, encoding="utf-8") as f:
        mygov = json.load(f)

    xizmatlar = mygov["xizmatlar"]
    for x in xizmatlar:
        qidiruv_matni = (
            x["xizmat_nomi"] + " " + " ".join(x["muammolar"]) + " " + x["tavsif"]
        )
        emb = embed(qidiruv_matni)
        collection.upsert(
            ids=["mygov-" + x["id"]],
            embeddings=[emb],
            documents=[json.dumps(x, ensure_ascii=False)],
        )
    print(f"my-gov: {len(xizmatlar)} ta xizmat indekslandi.")


if __name__ == "__main__":
    bazani_yuklash()
