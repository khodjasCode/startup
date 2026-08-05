import { useContext } from 'react'

import { ThemeContext } from './ThemeContext'
import type { ThemeContextValue } from './ThemeContext'

export function useTheme(): ThemeContextValue {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme faqat <ThemeProvider> ichida ishlatiladi.')
  }
  return context
}

export { ThemeProvider } from './ThemeProvider'
export { THEMES, applyTheme, readThemeChoice } from './theme'
export type { ResolvedTheme, ThemeChoice } from './theme'
