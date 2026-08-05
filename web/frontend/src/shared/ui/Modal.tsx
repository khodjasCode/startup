import { useEffect, useRef } from 'react'
import type { ReactNode } from 'react'
import { createPortal } from 'react-dom'

import { Icon } from './Icon'
import styles from './Modal.module.css'

interface ModalProps {
  title: string
  onClose: () => void
  closeLabel: string
  children: ReactNode
}

/** Oddiy modal oyna: fon, Escape bilan yopish va ochilganda fokusni ichkariga olish. */
export function Modal({ title, onClose, closeLabel, children }: ModalProps) {
  const boxRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKeyDown)

    const oldOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'

    boxRef.current?.querySelector<HTMLElement>('input, button, textarea, select')?.focus()

    return () => {
      document.removeEventListener('keydown', onKeyDown)
      document.body.style.overflow = oldOverflow
    }
  }, [onClose])

  return createPortal(
    <div className={styles.backdrop} onMouseDown={onClose}>
      <div
        ref={boxRef}
        className={styles.box}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        onMouseDown={(event) => event.stopPropagation()}
      >
        <header className={styles.head}>
          <h2 className={styles.title}>{title}</h2>
          <button type="button" className={styles.close} onClick={onClose} aria-label={closeLabel}>
            <Icon name="close" />
          </button>
        </header>
        <div className={styles.body}>{children}</div>
      </div>
    </div>,
    document.body,
  )
}
