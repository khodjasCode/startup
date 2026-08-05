/** Backend /api/katalog javoblari uchun tiplar (nomlar backend bilan bir xil). */

export interface Soha {
  nomi: string
  soni: number
}

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
