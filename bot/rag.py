# RAG yadro: savol → embedding → ChromaDB top-3 → Gemini Flash javobi

from google import genai
from google.genai import errors
import chromadb

from bot.config import (
    GEMINI_API_KEY,
    GEMINI_API_KEY_ZAXIRA,
    VEKTOR_BAZA_YOLI,
    EMBEDDING_MODEL,
    LLM_MODEL,
)
from bot.prompt import SYSTEM_PROMPT

# Asosiy va (bor bo'lsa) zaxira kalit bilan ikkita mijoz tayyorlab qo'yamiz —
# biri 429 (limit) qaytarsa, ikkinchisiga o'tiladi.
_KALITLAR = [k for k in (GEMINI_API_KEY, GEMINI_API_KEY_ZAXIRA) if k]
_MIJOZLAR = [genai.Client(api_key=kalit) for kalit in _KALITLAR]

chroma = chromadb.PersistentClient(path=str(VEKTOR_BAZA_YOLI))
collection = chroma.get_or_create_collection("idoralar")


class TokenlarTugadi(Exception):
    """Barcha Gemini API kalitlari so'rov limitiga (429) yetganda ko'tariladi."""


# Barcha kalitlar tugaganda foydalanuvchiga ko'rsatiladigan xabar — bot va
# web interfeysi ikkalasi ham shu matndan foydalanadi.
TOKENLAR_TUGADI_XABARI = (
    "💙 Hozircha sun'iy intellekt so'rovlari limiti to'lib qoldi — "
    "xizmatimiz bepul API asosida ishlaydi va kunlik so'rov chegarasi bor.\n\n"
    "⏳ Iltimos, birozdan so'ng qayta urinib ko'ring.\n\n"
    "🙏 Agar loyihamiz sizga foydali bo'lsa va uning yanada rivojlanishini, "
    "ko'proq odamlarga xizmat qila olishini istasangiz — ixtiyoriy homiylik "
    "(donat) qilib qo'llab-quvvatlashingiz mumkin. Har bir yordamingiz biz "
    "uchun katta ahamiyatga ega! 🚀✨"
)


def _kalitlar_bilan_urin(vazifa):
    """vazifa(mijoz) ni har bir mavjud kalit bilan navbatma-navbat sinaydi.
    429 (limit) bo'lsa keyingi kalitga o'tadi; boshqa xato bo'lsa darhol
    ko'taradi; barcha kalitlar 429 bersa TokenlarTugadi ko'taradi."""
    oxirgi_429 = None
    for mijoz in _MIJOZLAR:
        try:
            return vazifa(mijoz)
        except errors.ClientError as xato:
            if xato.code == 429:
                oxirgi_429 = xato
                continue
            raise
    raise TokenlarTugadi() from oxirgi_429


def embed(matn: str) -> list[float]:
    """Matnni embedding vektoriga aylantiradi (kalit-rotatsiya bilan).
    index_qurish.py ham, qidirish() ham shu funksiyadan foydalanadi —
    shunday qilib indekslash paytida ham 429 kelsa zaxira kalitga o'tiladi."""
    natija = _kalitlar_bilan_urin(
        lambda mijoz: mijoz.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=matn,
        )
    )
    return natija.embeddings[0].values


def qidirish(savol: str, k: int = 3) -> list[str]:
    emb = embed(savol)
    natija = collection.query(query_embeddings=[emb], n_results=k)
    return natija["documents"][0] if natija["documents"] else []


def javob_olish(savol_yoki_tarix) -> str:
    """savol_yoki_tarix: yagona savol matni (eski interfeys) yoki suhbat
    tarixi — [{"rol": "fuqaro"|"bot", "matn": str}, ...] ro'yxati, oxirgi
    element fuqaroning eng so'nggi xabari bo'lishi kerak. Tarix orqali bot
    "suv chiqmayapti" kabi noaniq savollarda aniqlashtiruvchi savol berib,
    keyingi xabarlar bilan to'ldirilgan kontekst asosida yakuniy javob beradi.

    Barcha Gemini API kalitlari so'rov limitiga yetsa TokenlarTugadi
    ko'tariladi — chaqiruvchi tomon buni alohida ushlab, foydalanuvchiga
    mos xabar ko'rsatishi kerak."""
    if isinstance(savol_yoki_tarix, str):
        tarix = [{"rol": "fuqaro", "matn": savol_yoki_tarix}]
    else:
        tarix = savol_yoki_tarix

    qidiruv_matni = "\n".join(x["matn"] for x in tarix if x["rol"] == "fuqaro")
    yozuvlar = qidirish(qidiruv_matni)
    kontekst = "\n---\n".join(yozuvlar) if yozuvlar else "(mos yozuv topilmadi)"

    contents = []
    oxirgi_fuqaro_indeksi = max(i for i, x in enumerate(tarix) if x["rol"] == "fuqaro")
    for i, xabar in enumerate(tarix):
        matn = xabar["matn"]
        if i == oxirgi_fuqaro_indeksi:
            matn = f"MA'LUMOT BAZASI YOZUVLARI:\n{kontekst}\n\nFUQARO SAVOLI: {matn}"
        rol = "user" if xabar["rol"] == "fuqaro" else "model"
        contents.append({"role": rol, "parts": [{"text": matn}]})

    resp = _kalitlar_bilan_urin(
        lambda mijoz: mijoz.models.generate_content(
            model=LLM_MODEL,
            config={"system_instruction": SYSTEM_PROMPT},
            contents=contents,
        )
    )
    return resp.text
