import { useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'

import { readStorage, writeStorage } from '@shared/lib/storage'

import { DEFAULT_LOCALE, LOCALE_STORAGE_KEY, isLocale } from './config'
import type { Locale } from './config'
import { DICTIONARIES } from './dictionaries'
import type { TranslationKey } from './dictionaries'
import { I18nContext } from './I18nContext'

function initialLocale(): Locale {
  const saved = readStorage(LOCALE_STORAGE_KEY)
  return isLocale(saved) ? saved : DEFAULT_LOCALE
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>(initialLocale)

  useEffect(() => {
    document.documentElement.lang = locale
  }, [locale])

  const setLocale = useCallback((next: Locale) => {
    setLocaleState(next)
    writeStorage(LOCALE_STORAGE_KEY, next)
  }, [])

  const value = useMemo(() => {
    const dictionary = DICTIONARIES[locale]
    const t = (key: TranslationKey) => dictionary[key] || DICTIONARIES[DEFAULT_LOCALE][key]
    return { locale, setLocale, t }
  }, [locale, setLocale])

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
}
