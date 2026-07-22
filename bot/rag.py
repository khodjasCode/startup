# RAG yadro: savol → embedding → ChromaDB top-3 → Gemini Flash javobi

from google import genai
import chromadb

from bot.config import GEMINI_API_KEY, VEKTOR_BAZA_YOLI, EMBEDDING_MODEL, LLM_MODEL
from bot.prompt import SYSTEM_PROMPT

client = genai.Client(api_key=GEMINI_API_KEY)
chroma = chromadb.PersistentClient(path=str(VEKTOR_BAZA_YOLI))
collection = chroma.get_or_create_collection("idoralar")


def qidirish(savol: str, k: int = 3) -> list[str]:
    emb = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=savol,
    ).embeddings[0].values
    natija = collection.query(query_embeddings=[emb], n_results=k)
    return natija["documents"][0] if natija["documents"] else []


def javob_olish(savol: str) -> str:
    yozuvlar = qidirish(savol)
    kontekst = "\n---\n".join(yozuvlar) if yozuvlar else "(mos yozuv topilmadi)"
    resp = client.models.generate_content(
        model=LLM_MODEL,
        config={"system_instruction": SYSTEM_PROMPT},
        contents=f"MA'LUMOT BAZASI YOZUVLARI:\n{kontekst}\n\nFUQARO SAVOLI: {savol}",
    )
    return resp.text
