import { useRef, useState } from 'react'
import type { FormEvent, KeyboardEvent } from 'react'

import { useI18n } from '@shared/i18n'

import styles from './ChatComposer.module.css'

interface ChatComposerProps {
  disabled: boolean
  onSubmit: (question: string) => void
}

export function ChatComposer({ disabled, onSubmit }: ChatComposerProps) {
  const { t } = useI18n()
  const [value, setValue] = useState('')
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const submit = (event: FormEvent) => {
    event.preventDefault()
    const question = value.trim()
    if (!question || disabled) return
    setValue('')
    onSubmit(question)
    inputRef.current?.focus()
  }

  // Enter — yuborish, Shift+Enter — yangi qator.
  const onKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      event.currentTarget.form?.requestSubmit()
    }
  }

  return (
    <form className={styles.form} onSubmit={submit}>
      <textarea
        ref={inputRef}
        className={styles.input}
        value={value}
        onChange={(event) => setValue(event.target.value)}
        onKeyDown={onKeyDown}
        placeholder={t('chat_placeholder')}
        aria-label={t('chat_placeholder')}
        rows={1}
      />
      <button type="submit" className={styles.send} disabled={disabled || !value.trim()}>
        {t('chat_send')}
      </button>
    </form>
  )
}
