# Demo ssenariy va prezentatsiya rejasi

**Muddat:** 2-avgust | **Format:** jonli demo (3 misol + 1 tuzoq) + slaydlar

## Jonli demo (5–6 daqiqa)

Oldindan tekshirib qo'yiladi: bot ishga tushgan, baza indekslangan, internet bor.
Zaxira: har bir misolning skrinshoti slaydlarda (agar jonli demo yiqilsa).

### 1-misol — Kommunal (elektr)
Yozamiz: `Mahallamizda har kuni kechqurun svet o'chib qolyapti, nima qilay?`
Ko'rsatamiz: bot idorani (tuman elektr tarmog'i), murojaat tartibini va manbani aytadi.
Gap: «Fuqaro qonun o'qimaydi — bot 10 soniyada yo'l ko'rsatadi».

### 2-misol — Mehnat (xato yozuv bilan!)
Yozamiz: `meni shartnomasiz ishlatishyapti zarplata ham kam berishyapti nima qilay`
Gap: «Xato yozuv, ruscha so'zlar aralash — semantik qidiruv baribir topadi».

### 3-misol — Kirillda (kadastr)
Yozamiz: `Мерос бўлиб қолган уйни ўз номимга рўйхатдан ўтказмоқчиман, нима қилишим керак?`
Gap: «Kirillda so'rasa — kirillda javob beradi».

### 4-misol — TUZOQ (eng kuchli lahza!)
Yozamiz: `Pasportimni yo'qotib qo'ydim, yangisini qanday olsam bo'ladi?`
Ko'rsatamiz: bot «aniq ma'lumotim yo'q» deb halol aytadi va my.gov.uz ga yo'naltiradi.
Gap: «Bot bilmagan narsani TO'QIMAYDI — bu bizning asosiy farqimiz ChatGPT'dan».

## Slaydlar rejasi (8–10 slayd)

1. **Muammo** — fuqaro qaysi idoraga borishni bilmaydi; pm.gov.uz ga millionlab murojaat, ko'pi noto'g'ri manzilga.
2. **Yechim** — Telegram-bot: muammoni oddiy tilda yoz → idora + tartib + hujjatlar + manba.
3. **Nega ishonchli** — RAG: faqat tekshirilgan bazadan javob; har javobda rasmiy manba; bilmasa — ochiq aytadi.
4. **Arxitektura** — savol → embedding → ChromaDB top-3 → Gemini (qat'iy prompt) → javob (README dagi sxema).
5. **Jonli demo** — yuqoridagi 4 misol.
6. **Sifat metrikalari** — qa/hisobot_*.md dan: top-3 aniqlik %, tuzoq savollarda 0 ta to'qilgan javob, N ta tekshirilgan yozuv.
7. **Real foydalanuvchi sinovi** — 10–15 kishi, % to'g'ri, % «borardim» (qa/foydalanuvchi_testi.md dan).
8. **Jamoa va rollar** — kim nima qildi.
9. **Keyingi rejalar** — baza 40–50 yozuvga, ovozli xabar, Yashil Makon moduli, viloyat kesimidagi kontaktlar.
10. **Savol-javob** — bot linki QR-kod bilan (zal o'zi sinab ko'rsin).

## Tayyorgarlik checklist

- [ ] Baza yozuvlari `tekshirilgan: true` (kamida demo'da ishlatiladigan 4 tasi)
- [ ] `python -m qa.baholash --javob` yakuniy hisobot olingan, raqamlar slaydda
- [ ] 4 demo misol jonli sinab ko'rilgan (demo kuni ertalab ham!)
- [ ] Skrinshot-zaxiralar slaydlarda
- [ ] QR-kod bot linkiga
- [ ] Gemini kunlik limiti tekshirilgan (demo oldidan ortiqcha so'rov yubormaslik)
