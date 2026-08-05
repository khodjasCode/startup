import { useSyncExternalStore } from 'react'

/** CSS media query holatini React state sifatida o'qish. */
export function useMediaQuery(query: string): boolean {
  const mql = typeof window === 'undefined' ? null : window.matchMedia(query)

  return useSyncExternalStore(
    (onChange) => {
      mql?.addEventListener('change', onChange)
      return () => mql?.removeEventListener('change', onChange)
    },
    () => mql?.matches ?? false,
    () => false,
  )
}
