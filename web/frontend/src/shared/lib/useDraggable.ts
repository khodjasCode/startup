import { useCallback, useRef, useState } from 'react'
import type { PointerEvent as ReactPointerEvent, RefObject } from 'react'

export interface Position {
  left: number
  top: number
}

interface DragState {
  pointerX: number
  pointerY: number
  left: number
  top: number
}

/**
 * Panelni "sarlavha satridan ushlab" ko'chirish. Element o'lchamlari CSS'da
 * qoladi, hook faqat joylashuvni (left/top) boshqaradi va uni ekran ichida
 * ushlab turadi. `enabled=false` bo'lsa (mobil to'liq ekran) hech narsa qilmaydi.
 */
export function useDraggable(elementRef: RefObject<HTMLElement | null>, enabled: boolean) {
  const [position, setPosition] = useState<Position | null>(null)
  const dragRef = useRef<DragState | null>(null)

  const clamp = useCallback(
    (left: number, top: number): Position => {
      const el = elementRef.current
      const maxLeft = Math.max(window.innerWidth - (el?.offsetWidth ?? 0), 0)
      const maxTop = Math.max(window.innerHeight - (el?.offsetHeight ?? 0), 0)
      return {
        left: Math.min(Math.max(left, 0), maxLeft),
        top: Math.min(Math.max(top, 0), maxTop),
      }
    },
    [elementRef],
  )

  const onPointerDown = useCallback(
    (event: ReactPointerEvent<HTMLElement>) => {
      if (!enabled || event.button !== 0) return
      // Sarlavhadagi tugmalar (yopish, kichraytirish...) ustidan boshlangan
      // bosish sudrash deb hisoblanmaydi — aks holda pointer capture tugmaning
      // click hodisasini o'g'irlab qo'yadi va tugmalar ishlamay qoladi.
      if (event.target instanceof Element && event.target.closest('[data-no-drag]')) return
      const el = elementRef.current
      if (!el) return

      const rect = el.getBoundingClientRect()
      dragRef.current = {
        pointerX: event.clientX,
        pointerY: event.clientY,
        left: rect.left,
        top: rect.top,
      }
      setPosition({ left: rect.left, top: rect.top })
      event.currentTarget.setPointerCapture(event.pointerId)
      event.preventDefault()
    },
    [elementRef, enabled],
  )

  const onPointerMove = useCallback(
    (event: ReactPointerEvent<HTMLElement>) => {
      const drag = dragRef.current
      if (!drag) return
      setPosition(
        clamp(
          drag.left + (event.clientX - drag.pointerX),
          drag.top + (event.clientY - drag.pointerY),
        ),
      )
    },
    [clamp],
  )

  const onPointerUp = useCallback((event: ReactPointerEvent<HTMLElement>) => {
    dragRef.current = null
    if (event.currentTarget.hasPointerCapture(event.pointerId)) {
      event.currentTarget.releasePointerCapture(event.pointerId)
    }
  }, [])

  const reset = useCallback(() => setPosition(null), [])

  return {
    position: enabled ? position : null,
    reset,
    handleProps: { onPointerDown, onPointerMove, onPointerUp, onPointerCancel: onPointerUp },
  }
}
