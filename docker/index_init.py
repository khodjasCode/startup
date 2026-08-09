# Konteyner ishga tushganda ChromaDB indeksi bo'sh bo'lsa, uni quradi.
# docker-compose'dagi bir martalik `index-init` xizmati shu skriptni ishga
# tushiradi; bot/web esa faqat tayyor indeksdan foydalanadi (bir vaqtda
# ikki jarayon bir xil vektor bazaga yozmasin deb).

from bot.index_qurish import bazani_yuklash
from bot.rag import collection

if collection.count() == 0:
    print("Vektor baza bo'sh — indekslanmoqda...", flush=True)
    bazani_yuklash()
    print(f"Tayyor: {collection.count()} yozuv indekslandi.", flush=True)
else:
    print(f"Vektor baza allaqachon tayyor ({collection.count()} yozuv).", flush=True)
