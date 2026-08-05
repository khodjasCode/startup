import { useI18n } from '@shared/i18n'

import type { ChatMessage } from '../model/types'
import { AnswerBody } from './AnswerBody'
import styles from './MessageBubble.module.css'

/**
 * Bitta xabar pufakchasi. Kutish va xatolik matnlari saqlanmaydi — joriy tilda
 * chiziladi, shuning uchun til almashtirilganda darhol yangilanadi.
 */
export function MessageBubble({ message }: { message: ChatMessage }) {
  const { t } = useI18n()

  if (message.role === 'user') {
    return <div className={`${styles.bubble} ${styles.user}`}>{message.text}</div>
  }

  if (message.status === 'pending') {
    return (
      <div className={`${styles.bubble} ${styles.bot} ${styles.muted}`} aria-live="polite">
        {t('chat_searching')}
      </div>
    )
  }

  if (message.status === 'error') {
    return <div className={`${styles.bubble} ${styles.bot} ${styles.muted}`}>{t('chat_error')}</div>
  }

  return (
    <div className={`${styles.bubble} ${styles.bot}`}>
      <AnswerBody text={message.text} />
    </div>
  )
}
