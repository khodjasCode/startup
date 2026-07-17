# QA baholash skripti: test_savollar.json bo'yicha sifat hisoboti
#
# Nimani o'lchaydi:
#   1. Qidiruv aniqligi (30 oddiy savol): kutilgan yozuv top-1 va top-3 da bormi.
#      Bu "nechta % to'g'ri idora" metrikasining asosi — javob top yozuvlarga tayanadi.
#   2. Tuzoq savollar (10 ta, --javob bilan): bot to'qib chiqarmasdan
#      "aniq ma'lumotim yo'q" deb my.gov.uz/pm.gov.uz ga yo'naltiradimi.
#
# Ishga tushirish (GEMINI_API_KEY .env dan o'zi olinadi, BOT_TOKEN kerak EMAS):
#   python3 -m qa.baholash            # faqat qidiruv aniqligi (~30 soniya)
#   python3 -m qa.baholash --javob    # + tuzoq savollarga LLM javoblari (~3 daqiqa,
#                                     #   bepul tier limiti 5 so'rov/daqiqa bo'lgani uchun sekin)
#
# Natija: qa/hisobot_YYYY-MM-DD.md (xato bo'lsa ham qisman hisobot yoziladi)

import argparse
import json
import os
import time
from datetime import date

# config.py BOT_TOKEN ni talab qiladi, lekin baholashga Telegram kerak emas
os.environ.setdefault("BOT_TOKEN", "qa-baholash-uchun-kerak-emas")

from bot.config import LOYIHA_ILDIZI
from bot.rag import qidirish, javob_olish, collection

SAVOLLAR_YOLI = LOYIHA_ILDIZI / "qa" / "test_savollar.json"

# Tuzoq savolga "halol" javob belgilari (lotin va kirill)
HALOLLIK_BELGILARI = [
    "ma'lumotim yo'q", "maʼlumotim yo'q", "ma'lumot yo'q",
    "маълумотим йўқ", "маълумот йўқ",
    "my.gov.uz", "pm.gov.uz",
]

LLM_ORASIDAGI_PAUZA = 13  # soniya; bepul tier: gemini-2.5-flash uchun 5 so'rov/daqiqa


def limit_bilan(fn, *args, urinishlar: int = 4):
    """API limiti (429) yoki vaqtinchalik bandlik (503) bo'lsa 30 soniya kutib qayta urinadi."""
    for i in range(urinishlar):
        try:
            return fn(*args)
        except Exception as e:
            oxirgi = i == urinishlar - 1
            vaqtinchalik = any(t in str(e) for t in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"))
            if vaqtinchalik and not oxirgi:
                print("    ... vaqtinchalik xato (429/503), 30 soniya kutilmoqda")
                time.sleep(30)
            else:
                raise


def indeks_tayyorlash():
    if collection.count() == 0:
        print("Vektor baza bo'sh — indekslanmoqda...")
        from bot.index_qurish import bazani_yuklash
        bazani_yuklash()


def topilgan_idlar(savol: str) -> list[str]:
    """Qidiruv natijasidagi hujjatlardan yozuv id'larini ajratadi."""
    idlar = []
    for hujjat in limit_bilan(qidirish, savol):
        try:
            idlar.append(json.loads(hujjat)["id"])
        except (json.JSONDecodeError, KeyError):
            idlar.append("(id o'qilmadi)")
    return idlar


def qidiruv_baholash(savollar: list[dict]) -> list[dict]:
    natijalar = []
    for s in savollar:
        try:
            idlar = topilgan_idlar(s["savol"])
            xato = None
        except Exception as e:
            idlar, xato = [], str(e)[:200]
        natijalar.append({
            **s,
            "topilgan": idlar,
            "top1": bool(idlar) and idlar[0] == s["kutilgan_id"],
            "top3": s["kutilgan_id"] in idlar,
            "xato": xato,
        })
        belgi = "✅" if natijalar[-1]["top3"] else ("💥" if xato else "❌")
        print(f"  {s['id']} {belgi} kutilgan={s['kutilgan_id']} topilgan={idlar or xato}")
        time.sleep(0.5)
    return natijalar


def tuzoq_baholash(savollar: list[dict]) -> list[dict]:
    natijalar = []
    for n, s in enumerate(savollar):
        try:
            javob = limit_bilan(javob_olish, s["savol"])
            halol = any(b in javob.lower() for b in HALOLLIK_BELGILARI)
            belgi = "✅" if halol else "⚠️"
        except Exception as e:
            javob, halol, belgi = f"(XATO: {str(e)[:200]})", False, "💥"
        natijalar.append({**s, "javob": javob, "halol_avto": halol})
        print(f"  {s['id']} {belgi} (avto-tekshiruv)")
        if n < len(savollar) - 1:
            time.sleep(LLM_ORASIDAGI_PAUZA)
    return natijalar


def foiz(qism: int, jami: int) -> str:
    return f"{100 * qism / jami:.0f}%" if jami else "—"


def hisobot_yozish(qidiruv: list[dict], tuzoq: list[dict], javob_rejimi: bool) -> str:
    bugun = date.today().isoformat()
    yol = LOYIHA_ILDIZI / "qa" / f"hisobot_{bugun}.md"

    jami = len(qidiruv)
    top1 = sum(n["top1"] for n in qidiruv)
    top3 = sum(n["top3"] for n in qidiruv)

    qatorlar = [
        f"# Sifat hisoboti — {bugun}",
        "",
        "## Qidiruv aniqligi (to'g'ri idora topildimi)",
        "",
        f"- **Top-1:** {top1}/{jami} ({foiz(top1, jami)})",
        f"- **Top-3:** {top3}/{jami} ({foiz(top3, jami)}) — javob top-3 yozuvga tayanadi",
        f"- Maqsad (ISH_REJA): ≥ 80% — {'✅ BAJARILDI' if jami and top3 / jami >= 0.8 else '❌ HALI YETILMADI'}",
        "",
        "### Savol turi bo'yicha",
        "",
        "| Tur | Top-3 | Foiz |",
        "|---|---|---|",
    ]
    for tur in ("oddiy", "xato_yozuv", "kirill"):
        guruh = [n for n in qidiruv if n["tur"] == tur]
        t3 = sum(n["top3"] for n in guruh)
        qatorlar.append(f"| {tur} | {t3}/{len(guruh)} | {foiz(t3, len(guruh))} |")

    qatorlar += [
        "",
        "### Savollar kesimida",
        "",
        "| # | Tur | Kutilgan | Top-1 | Top-3 | Topilgan (tartibda) |",
        "|---|---|---|---|---|---|",
    ]
    for n in qidiruv:
        topilgan = ", ".join(n["topilgan"]) if n["topilgan"] else f"XATO: {n['xato']}"
        qatorlar.append(
            f"| {n['id']} | {n['tur']} | {n['kutilgan_id']} "
            f"| {'✅' if n['top1'] else '❌'} | {'✅' if n['top3'] else '❌'} "
            f"| {topilgan} |"
        )

    qatorlar += ["", "## Tuzoq savollar (gallyutsinatsiya tekshiruvi)", ""]
    if tuzoq:
        halol = sum(n["halol_avto"] for n in tuzoq)
        qatorlar += [
            f"- Avto-tekshiruvdan o'tdi: {halol}/{len(tuzoq)} ({foiz(halol, len(tuzoq))})",
            "- Avto-tekshiruv faqat belgi so'zlarni qidiradi — har bir javobni QO'LDA ham o'qib chiqing:",
            "  idora nomi/telefon/muddat to'qilmaganligiga ishonch hosil qiling.",
            "",
        ]
        for n in tuzoq:
            qatorlar += [
                f"### {n['id']} — {'✅ halol (avto)' if n['halol_avto'] else '⚠️ QO`LDA TEKSHIRILSIN'}",
                "",
                f"**Savol:** {n['savol']}",
                "",
                "**Javob:**",
                "",
                "> " + n["javob"].replace("\n", "\n> "),
                "",
            ]
    elif javob_rejimi:
        qatorlar.append("Natija yo'q (jarayon boshida uzilgan bo'lishi mumkin).")
    else:
        qatorlar.append("O'tkazilmadi (`--javob` bayrog'isiz ishga tushirilgan).")

    yol.write_text("\n".join(qatorlar) + "\n", encoding="utf-8")
    return str(yol)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG sifatini baholash")
    parser.add_argument("--javob", action="store_true",
                        help="tuzoq savollarga to'liq LLM javoblarini ham olish")
    args = parser.parse_args()

    with open(SAVOLLAR_YOLI, encoding="utf-8") as f:
        hamma = json.load(f)["savollar"]
    oddiy = [s for s in hamma if s["tur"] != "tuzoq"]
    tuzoqlar = [s for s in hamma if s["tur"] == "tuzoq"]

    indeks_tayyorlash()

    qidiruv_natija, tuzoq_natija = [], []
    try:
        print(f"\nQidiruv aniqligi ({len(oddiy)} savol):")
        qidiruv_natija = qidiruv_baholash(oddiy)

        if args.javob:
            print(f"\nTuzoq savollar ({len(tuzoqlar)} savol, LLM bilan, "
                  f"har biriga ~{LLM_ORASIDAGI_PAUZA} soniya pauza):")
            tuzoq_natija = tuzoq_baholash(tuzoqlar)
    finally:
        if qidiruv_natija or tuzoq_natija:
            yol = hisobot_yozish(qidiruv_natija, tuzoq_natija, args.javob)
            print(f"\nHisobot yozildi: {yol}")
