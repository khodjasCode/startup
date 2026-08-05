import { useEffect, useRef } from 'react'

import { useI18n } from '@shared/i18n'

import type { ChatMessage } from '../model/types'
import { MessageBubble } from './MessageBubble'
import styles from './MessageList.module.css'

export function MessageList({ messages }: { messages: ChatMessage[] }) {
  const { t } = useI18n()
  const listRef = useRef<HTMLDivElement>(null)

  // Har bir yangi xabardan keyin pastga tushamiz.
  useEffect(() => {
    const el = listRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [messages])

  return (
    <div ref={listRef} className={styles.list} role="log" aria-label={t('chat_log')}>
      {messages.length === 0 ? (
        <div className={styles.greeting}>{t('chat_greeting')}</div>
      ) : (
        messages.map((message) => <MessageBubble key={message.id} message={message} />)
      )}
    </div>
  )
}
