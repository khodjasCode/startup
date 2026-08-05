import { useEffect } from 'react'
import type { RefObject } from 'react'

/** Element tashqarisiga bosilganda (yoki Escape bosilganda) handler chaqiriladi. */
export function useOnClickOutside(
  ref: RefObject<HTMLElement | null>,
  handler: () => void,
  enabled = true,
): void {
  useEffect(() => {
    if (!enabled) return

    const onPointerDown = (event: MouseEvent | TouchEvent) => {
      const el = ref.current
      if (el && event.target instanceof Node && !el.contains(event.target)) handler()
    }
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') handler()
    }

    document.addEventListener('mousedown', onPointerDown)
    document.addEventListener('touchstart', onPointerDown)
    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('mousedown', onPointerDown)
      document.removeEventListener('touchstart', onPointerDown)
      document.removeEventListener('keydown', onKeyDown)
    }
  }, [ref, handler, enabled])
}
