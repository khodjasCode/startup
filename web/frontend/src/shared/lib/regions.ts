import type { Locale } from '@shared/i18n'

/**
 * O'zbekiston hududlari: 12 viloyat + Qoraqalpog'iston Respublikasi +
 * Toshkent shahri.
 *
 * Diqqat: butun O'zbekiston bitta vaqt mintaqasida (UTC+5, yozgi vaqtsiz),
 * shuning uchun hudud tanlash soatdagi **yozuvni** o'zgartiradi, vaqtning
 * o'zini emas.
 */
export interface Region {
  id: string
  nomi: Record<Locale, string>
}

export const REGIONS: Region[] = [
  { id: 'toshkent-shahri', nomi: { uz: 'Toshkent shahri', ru: 'город Ташкент', en: 'Tashkent city' } },
  { id: 'toshkent', nomi: { uz: 'Toshkent viloyati', ru: 'Ташкентская область', en: 'Tashkent region' } },
  { id: 'andijon', nomi: { uz: 'Andijon', ru: 'Андижанская область', en: 'Andijan' } },
  { id: 'buxoro', nomi: { uz: 'Buxoro', ru: 'Бухарская область', en: 'Bukhara' } },
  { id: 'fargona', nomi: { uz: "Farg'ona", ru: 'Ферганская область', en: 'Fergana' } },
  { id: 'jizzax', nomi: { uz: 'Jizzax', ru: 'Джизакская область', en: 'Jizzakh' } },
  { id: 'namangan', nomi: { uz: 'Namangan', ru: 'Наманганская область', en: 'Namangan' } },
  { id: 'navoiy', nomi: { uz: 'Navoiy', ru: 'Навоийская область', en: 'Navoiy' } },
  { id: 'qashqadaryo', nomi: { uz: 'Qashqadaryo', ru: 'Кашкадарьинская область', en: 'Kashkadarya' } },
  { id: 'samarqand', nomi: { uz: 'Samarqand', ru: 'Самаркандская область', en: 'Samarkand' } },
  { id: 'sirdaryo', nomi: { uz: 'Sirdaryo', ru: 'Сырдарьинская область', en: 'Syrdarya' } },
  { id: 'surxondaryo', nomi: { uz: 'Surxondaryo', ru: 'Сурхандарьинская область', en: 'Surkhandarya' } },
  { id: 'xorazm', nomi: { uz: 'Xorazm', ru: 'Хорезмская область', en: 'Khorezm' } },
  {
    id: 'qoraqalpogiston',
    nomi: {
      uz: "Qoraqalpog'iston Respublikasi",
      ru: 'Республика Каракалпакстан',
      en: 'Republic of Karakalpakstan',
    },
  },
]

export const DEFAULT_REGION = 'toshkent-shahri'

export function regionNomi(id: string, locale: Locale): string {
  const region = REGIONS.find((item) => item.id === id)
  return region ? region.nomi[locale] : ''
}
