import { createContext } from 'react'

import type { ResolvedTheme, ThemeChoice } from './theme'

export interface ThemeContextValue {
  choice: ThemeChoice
  resolved: ResolvedTheme
  setChoice: (choice: ThemeChoice) => void
}

export const ThemeContext = createContext<ThemeContextValue | null>(null)
