# Indekslash skripti: bilim_bazasi.json → ChromaDB
# Ishga tushirish:  python -m bot.index_qurish

import json

from bot.config import BILIM_BAZASI_YOLI, EMBEDDING_MODEL
from bot.rag import client, collection


def bazani_yuklash():
    """bilim_bazasi.json dagi tekshirilgan yozuvlarni ChromaDB ga indekslaydi."""
    with open(BILIM_BAZASI_YOLI, encoding="utf-8") as f:
        data = json.load(f)

    yozuvlar = [y for y in data["yozuvlar"]]  # MVP test uchun hammasi;
    # ishga chiqarishda: [y for y in data["yozuvlar"] if y["tekshirilgan"]]

    for y in yozuvlar:
        qidiruv_matni = y["muammo"] + " " + " ".join(y["kalit_sozlar"])
        emb = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=qidiruv_matni,
        ).embeddings[0].values
        collection.upsert(
            ids=[y["id"]],
            embeddings=[emb],
            documents=[json.dumps(y, ensure_ascii=False)],
        )
    print(f"{len(yozuvlar)} ta yozuv indekslandi.")


if __name__ == "__main__":
    bazani_yuklash()
