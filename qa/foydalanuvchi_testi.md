UM — QA + Demo (sifat va taqdimot)
Test-savollar to'plami (shu jumladan 10 ta "tuzoq" savol), real foydalanuvchi testi, prezentatsiya
12-iyul: 30 ta test-savol tayyor (xato yozilgan, kirillcha variantlar bilan)
19-iyul: birinchi sifat hisoboti (nechta % to'g'ri idora)
26-iyul: 10–15 real foydalanuvchi sinovi, bug ro'yxati IK/AK ga
2-avgust: demo ssenariy (3 jonli misol) + slaydlar tayyor# Real foydalanuvchi sinovi — reja va bug ro'yxati

**Muddat:** 26-iyulgacha | **Maqsad:** 10–15 real foydalanuvchi, bug ro'yxati IK/AK ga

## Sinov tartibi

1. Har bir sinovchi botga **kamida 3 ta savol** beradi:
   - bittasi o'z hayotidan real muammo (biz aytmaymiz — o'zi o'ylab topadi);
   - bittasi kirillda yoki xato yozuv bilan;
   - bittasi bazada bo'lmasligi mumkin bo'lgan mavzu (tuzoq-holat kuzatuvi).
2. Sinovchidan so'raymiz: «Bot aytgan idoraga chindan borarmiding?» (ha/yo'q/ishonmadim).
3. Har bir sessiya quyidagi jadvalga yoziladi (skrinshot bilan).
4. Sinovchilar tarkibi har xil bo'lsin: kamida 3 nafar 40+ yoshli, kamida 3 nafar faqat kirillda yozadigan.

## Natijalar jadvali

| # | Sana | Sinovchi (yosh/kasb) | Savol | Bot javobi to'g'rimi | Ishonch (borarmidi) | Izoh |
|---|------|----------------------|-------|----------------------|---------------------|------|
| 1 |      |                      |       |                      |                     |      |

## Bug ro'yxati (IK/AK ga topshiriladi)

Jiddiylik: **KRITIK** — noto'g'ri idora/to'qilgan ma'lumot; **O'RTA** — noqulay javob, alifbo xatosi, sekinlik; **PAST** — matn/formatlash.

| # | Sana | Savol (aynan) | Kutilgan | Bot bergan | Jiddiylik | Kimga (IK/AK) | Holat |
|---|------|---------------|----------|------------|-----------|----------------|-------|
| B1 | 2026-07-17 | X07: Harbiy xizmatdan kechiktirish (otsrochka)... | "Ma'lumotim yo'q" + my.gov.uz/pm.gov.uz, boshqa hech narsa | "Ma'lumotim yo'q" DEDI, lekin baribir aniq qaror raqami (445-son, 2017) va lex.uz havolasini O'ZIDAN QO'SHDI — bu tekshirilmagan ma'lumot, havola noto'g'ri bo'lishi mumkin | KRITIK | AK (prompt) | ochiq |
| B2 | 2026-07-17 | X03: Haydovchilik guvohnomasi olish... | Faqat "ma'lumotim yo'q" + portallar | Javobga bazada yo'q "YHXBB" idorasini qo'shdi | O'RTA | AK (prompt) | ochiq |
| B3 |     |               |          |            |           |                | ochiq |

**B1/B2 uchun taklif (prompt.py, 3-qoidaga qo'shimcha):** "Qonun, qaror raqami yoki internet-havolani ham o'zingdan qo'shma — faqat yozuvlardagi manbani keltir." Tuzatishdan keyin `python3 -m qa.baholash --javob` qayta o'tkazilsin.

## Sinovdan keyin

- KRITIK buglar demo'gacha yopilishi SHART.
- Feedback bo'yicha `data/bilim_bazasi.json` ga yangi `kalit_sozlar` qo'shiladi (xato yozuvlar aynan sinovdagidek).
- Yakuniy metrikalar prezentatsiyaga: nechta sinovchi, nechta savol, % to'g'ri, % ishonch.
