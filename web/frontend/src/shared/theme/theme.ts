import { readStorage, writeStorage } from '@shared/lib/storage'

/** Foydalanuvchi tanlovi: aniq mavzu yoki tizim sozlamasiga ergashish. */
export const THEMES = ['system', 'light', 'dark'] as const
export type ThemeChoice = (typeof THEMES)[number]

/** Haqiqatda qo'llanadigan mavzu. */
export type ResolvedTheme = 'light' | 'dark'

export const THEME_STORAGE_KEY = 'compass:theme'

export function isThemeChoice(value: unknown): value is ThemeChoice {
  return typeof value === 'string' && (THEMES as readonly string[]).includes(value)
}

export function readThemeChoice(): ThemeChoice {
  const saved = readStorage(THEME_STORAGE_KEY)
  return isThemeChoice(saved) ? saved : 'system'
}

export function systemTheme(): ResolvedTheme {
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export function resolveTheme(choice: ThemeChoice): ResolvedTheme {
  return choice === 'system' ? systemTheme() : choice
}

/**
 * <html data-theme="..."> ni yangilaydi. React render'idan oldin ham
 * chaqiriladi (main.tsx) — shu sababli sahifa boshidanoq to'g'ri rangda chiziladi.
 */
export function applyTheme(choice: ThemeChoice): ResolvedTheme {
  const resolved = resolveTheme(choice)
  document.documentElement.dataset['theme'] = resolved
  return resolved
}

export function saveThemeChoice(choice: ThemeChoice): void {
  writeStorage(THEME_STORAGE_KEY, choice)
}
