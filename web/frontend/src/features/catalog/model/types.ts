/** Backend /api/katalog javoblari uchun tiplar (nomlar backend bilan bir xil). */

export interface Soha {
  nomi: string
  soni: number
}

/** Bitta tildagi tarjima qilingan maydonlar to'plami (ru yoki en). */
export interface XizmatI18n {
  nomi: string
  tavsif: string
  muammolar: string[]
  qadamlar: string[]
  hujjatlar: string[]
  muddat: string
  narx: string
  aloqa: string
  kimlar_uchun: string
  idora: string
  qoshimcha: string
}

/** Rus/ingliz tarjimasi mavjud bo'lsa; bo'lmasa backend `null` qaytaradi. */
export type XizmatTarjimasi = { ru: XizmatI18n; en: XizmatI18n } | null

export interface XizmatQisqa {
  id: string
  manba: string
  soha: string
  nomi: string
  tavsif: string
  url: string
  /** Yozuv savol-javob ko'rinishidami (xizmat emas). */
  faq: boolean
  /** Savol-javoblar uchun mavzu guruhi. */
  kategoriya: string
  i18n: XizmatTarjimasi
}

export interface Xizmat extends XizmatQisqa {
  muammolar: string[]
  qadamlar: string[]
  hujjatlar: string[]
  muddat: string
  narx: string
  aloqa: string
  kimlar_uchun: string
  idora: string
  qoshimcha: string
}

export interface Manba {
  kalit: string
  nomi: string
  url: string
  tavsif: string
  aloqa: string
  kirish_tartibi: string[]
  yigilgan_sana: string
  xizmatlar_soni: number
}

export interface SavolJavob {
  id: string
  savol: string
  javob: string
  izoh: string
  url: string
  i18n: XizmatTarjimasi
}

/** Savol-javoblar mavzu bloklariga guruhlangan holda keladi. */
export interface FaqGuruhi {
  nomi: string
  soni: number
  savollar: SavolJavob[]
}

export interface Statistika {
  jami_yozuvlar: number
  sohalar_soni: number
  faq_soni: number
  manbalar: Manba[]
}
