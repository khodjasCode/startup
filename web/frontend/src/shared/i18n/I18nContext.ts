import { createContext } from 'react'

import type { Locale } from './config'
import type { TranslationKey } from './dictionaries'

export interface I18nContextValue {
  locale: Locale
  setLocale: (locale: Locale) => void
  /** Kalit bo'yicha joriy tildagi matn (kalit topilmasa — o'zbekchasi). */
  t: (key: TranslationKey) => string
}

export const I18nContext = createContext<I18nContextValue | null>(null)
