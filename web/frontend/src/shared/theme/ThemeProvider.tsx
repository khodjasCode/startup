import { useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'

import { ThemeContext } from './ThemeContext'
import { applyTheme, readThemeChoice, resolveTheme, saveThemeChoice } from './theme'
import type { ThemeChoice } from './theme'

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [choice, setChoiceState] = useState<ThemeChoice>(readThemeChoice)
  const [resolved, setResolved] = useState(() => resolveTheme(choice))

  // "system" tanlangan bo'lsa, tizim mavzusi almashganda darhol ergashamiz.
  useEffect(() => {
    setResolved(applyTheme(choice))
    if (choice !== 'system') return

    const media = window.matchMedia('(prefers-color-scheme: dark)')
    const onChange = () => setResolved(applyTheme('system'))
    media.addEventListener('change', onChange)
    return () => media.removeEventListener('change', onChange)
  }, [choice])

  const setChoice = useCallback((next: ThemeChoice) => {
    saveThemeChoice(next)
    setChoiceState(next)
  }, [])

  const value = useMemo(() => ({ choice, resolved, setChoice }), [choice, resolved, setChoice])

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}
