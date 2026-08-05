import type { Locale } from '@shared/i18n'

import type { SavolJavob, Xizmat, XizmatQisqa } from '@features/catalog'

/**
 * Bazadagi asl matnlar faqat o'zbekcha (my.gov.uz, lex.uz va h.k. shu tilda
 * yig'ilgan) — ru/en tarjimasi backend'dan har bir yozuvning `i18n` maydonida
 * keladi. Bu funksiyalar joriy tilga qarab ko'rsatiladigan matnni tanlaydi:
 * tarjima bo'lsa va til o'zbekcha bo'lmasa — tarjima, aks holda asl (uz) matn.
 */

/** Ro'yxatlarda ishlatiladigan qisqa shakl: faqat nomi/tavsif tarjima qilinadi. */
export function localizeXizmatQisqa<T extends XizmatQisqa>(xizmat: T, locale: Locale): T {
  const tarjima = locale !== 'uz' ? xizmat.i18n?.[locale] : undefined
  if (!tarjima) return xizmat
  return {
    ...xizmat,
    nomi: tarjima.nomi || xizmat.nomi,
    tavsif: tarjima.tavsif || xizmat.tavsif,
  }
}

/** Xizmat sahifasidagi to'liq shakl: barcha matn maydonlari tarjima qilinadi. */
export function localizeXizmat(xizmat: Xizmat, locale: Locale): Xizmat {
  const tarjima = locale !== 'uz' ? xizmat.i18n?.[locale] : undefined
  if (!tarjima) return xizmat
  return {
    ...xizmat,
    nomi: tarjima.nomi || xizmat.nomi,
    tavsif: tarjima.tavsif || xizmat.tavsif,
    muammolar: tarjima.muammolar.length ? tarjima.muammolar : xizmat.muammolar,
    qadamlar: tarjima.qadamlar.length ? tarjima.qadamlar : xizmat.qadamlar,
    hujjatlar: tarjima.hujjatlar.length ? tarjima.hujjatlar : xizmat.hujjatlar,
    muddat: tarjima.muddat || xizmat.muddat,
    narx: tarjima.narx || xizmat.narx,
    aloqa: tarjima.aloqa || xizmat.aloqa,
    kimlar_uchun: tarjima.kimlar_uchun || xizmat.kimlar_uchun,
    idora: tarjima.idora || xizmat.idora,
    qoshimcha: tarjima.qoshimcha || xizmat.qoshimcha,
  }
}

export function localizeSavolJavob(item: SavolJavob, locale: Locale): SavolJavob {
  const tarjima = locale !== 'uz' ? item.i18n?.[locale] : undefined
  if (!tarjima) return item
  return {
    ...item,
    savol: tarjima.nomi || item.savol,
    javob: tarjima.tavsif || item.javob,
    izoh: tarjima.qoshimcha || item.izoh,
  }
}
