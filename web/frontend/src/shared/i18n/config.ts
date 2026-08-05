export const LOCALES = ['uz', 'ru', 'en'] as const

export type Locale = (typeof LOCALES)[number]

export const DEFAULT_LOCALE: Locale = 'uz'

/** Til tanlovi shu kalit ostida localStorage'da saqlanadi. */
export const LOCALE_STORAGE_KEY = 'compass:locale'

/** Til tugmasidagi qisqa yorliq va menyudagi to'liq nom. */
export const LOCALE_LABELS: Record<Locale, { short: string; full: string }> = {
  uz: { short: 'UZB', full: "O'zbekcha" },
  ru: { short: 'RU', full: 'Русский' },
  en: { short: 'EN', full: 'English' },
}

export function isLocale(value: unknown): value is Locale {
  return typeof value === 'string' && (LOCALES as readonly string[]).includes(value)
}
