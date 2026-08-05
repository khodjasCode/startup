import type { FaqGuruhi, Manba, Soha, Statistika, Xizmat } from '../model/types'

/** /data/katalog.json — `python -m web.eksport_katalog` yaratadigan fayl. */
interface KatalogFayli {
  sohalar: Soha[]
  manbalar: Manba[]
  statistika: Omit<Statistika, 'manbalar'>
  xizmatlar: Xizmat[]
}

const FAQ_BOSHQA = 'Boshqa savollar'

let kesh: Promise<KatalogFayli> | null = null

/** Fayl bir marta yuklanadi va keshlanadi (backend o'chiq bo'lgan holat uchun). */
function yuklash(): Promise<KatalogFayli> {
  kesh ??= fetch('/data/katalog.json').then((javob) => {
    if (!javob.ok) throw new Error(`katalog.json: ${javob.status}`)
    return javob.json() as Promise<KatalogFayli>
  })
  return kesh
}

function mos(xizmat: Xizmat, soha: string, matn: string): boolean {
  if (soha && xizmat.soha !== soha) return false
  const kalit = matn.trim().toLowerCase()
  if (!kalit) return true
  return (
    xizmat.nomi.toLowerCase().includes(kalit) ||
    xizmat.tavsif.toLowerCase().includes(kalit) ||
    xizmat.muammolar.some((muammo) => muammo.toLowerCase().includes(kalit))
  )
}

/**
 * Backenddagi /api/... bilan bir xil natijani beradigan zaxira manba.
 * Filtrlash va guruhlash brauzerda bajariladi.
 */
export const staticKatalog = {
  async sohalar(): Promise<Soha[]> {
    return (await yuklash()).sohalar
  },

  async manbalar(): Promise<Manba[]> {
    return (await yuklash()).manbalar
  },

  async statistika(): Promise<Statistika> {
    const fayl = await yuklash()
    return { ...fayl.statistika, manbalar: fayl.manbalar }
  },

  async xizmatlar({
    soha = '',
    q = '',
    limit = 24,
    offset = 0,
  }: {
    soha?: string
    q?: string
    limit?: number
    offset?: number
  }) {
    const fayl = await yuklash()
    const topildi = fayl.xizmatlar.filter((xizmat) => !xizmat.faq && mos(xizmat, soha, q))
    return { jami: topildi.length, xizmatlar: topildi.slice(offset, offset + limit) }
  },

  async xizmat(id: string): Promise<Xizmat> {
    const fayl = await yuklash()
    const topildi = fayl.xizmatlar.find((xizmat) => xizmat.id === id)
    if (!topildi) throw new Error('Xizmat topilmadi')
    return topildi
  },

  async savolJavob({ q = '' }: { q?: string }): Promise<{ jami: number; guruhlar: FaqGuruhi[] }> {
    const fayl = await yuklash()
    const topildi = fayl.xizmatlar.filter((xizmat) => xizmat.faq && mos(xizmat, '', q))

    const guruhlar = new Map<string, Xizmat[]>()
    for (const yozuv of topildi) {
      const nomi = yozuv.kategoriya || (yozuv.manba === 'savol-javob' ? FAQ_BOSHQA : yozuv.soha)
      const mavjud = guruhlar.get(nomi)
      if (mavjud) mavjud.push(yozuv)
      else guruhlar.set(nomi, [yozuv])
    }

    const royxat: FaqGuruhi[] = [...guruhlar.entries()]
      .sort((a, b) => {
        // "Boshqa savollar" doim oxirida.
        if ((a[0] === FAQ_BOSHQA) !== (b[0] === FAQ_BOSHQA)) return a[0] === FAQ_BOSHQA ? 1 : -1
        return b[1].length - a[1].length || a[0].localeCompare(b[0])
      })
      .map(([nomi, yozuvlar]) => ({
        nomi,
        soni: yozuvlar.length,
        savollar: yozuvlar.map((y) => ({
          id: y.id,
          savol: y.nomi,
          javob: y.tavsif,
          izoh: y.qoshimcha,
          url: y.url,
          i18n: y.i18n,
        })),
      }))

    return { jami: topildi.length, guruhlar: royxat }
  },
}
