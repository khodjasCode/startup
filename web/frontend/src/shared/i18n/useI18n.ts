import { useContext } from 'react'

import { I18nContext } from './I18nContext'
import type { I18nContextValue } from './I18nContext'

export function useI18n(): I18nContextValue {
  const context = useContext(I18nContext)
  if (!context) {
    throw new Error('useI18n faqat <I18nProvider> ichida ishlatiladi.')
  }
  return context
}
