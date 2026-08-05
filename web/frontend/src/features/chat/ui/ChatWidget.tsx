import { useEffect, useRef } from 'react'

import { useI18n } from '@shared/i18n'
import { cx } from '@shared/lib/cx'
import { useDraggable } from '@shared/lib/useDraggable'
import { useMediaQuery } from '@shared/lib/useMediaQuery'
import { Icon } from '@shared/ui/Icon'

import { useChat } from '../model/useChat'
import { ChatComposer } from './ChatComposer'
import { ChatSessions } from './ChatSessions'
import styles from './ChatWidget.module.css'
import { MessageList } from './MessageList'

/**
 * Chat paneli — ilova ichidagi oddiy komponent (iframe emas), shuning uchun til
 * va suhbat holati sayt bilan bir manbadan keladi.
 *
 * Ikki ko'rinishi bor:
 *  · oyna    — pastki-o'ng burchakdagi tor panel, sarlavhasidan sudrab ko'chiriladi;
 *  · yoyilgan — o'ng chetga sarlavhadan pastgacha o'rnashadi va ichida
 *               suhbatlar ro'yxati (mini-panel) ochiladi.
 */
export function ChatWidget() {
  const { t } = useI18n()
  const { messages, isBusy, isOpen, isExpanded, close, toggleExpanded, ask } = useChat()

  const panelRef = useRef<HTMLElement>(null)
  const isDesktop = useMediaQuery('(min-width: 601px)')
  const suriladi = isDesktop && !isExpanded
  const { position, reset, handleProps } = useDraggable(panelRef, suriladi)

  // Yoyilgan yoki mobil ko'rinishda surilgan joylashuv ma'nosini yo'qotadi.
  useEffect(() => {
    if (!suriladi) reset()
  }, [suriladi, reset])

  // Yoyilgan holatda Escape — oynaga qaytarish.
  useEffect(() => {
    if (!isExpanded) return
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') toggleExpanded()
    }
    document.addEventListener('keydown', onKeyDown)
    return () => document.removeEventListener('keydown', onKeyDown)
  }, [isExpanded, toggleExpanded])

  if (!isOpen) return null

  return (
    <section
      ref={panelRef}
      className={cx(styles.panel, isExpanded && styles.expanded)}
      style={
        position && suriladi
          ? { left: position.left, top: position.top, right: 'auto', bottom: 'auto' }
          : undefined
      }
      aria-label={t('chat_title')}
    >
      <header className={styles.header} {...handleProps}>
        <span className={styles.title}>
          <img src="/images/ai-logo.png" alt="" className={styles.avatar} />
          {t('chat_title')}
        </span>
        {/* data-no-drag: bu tugmalar ustidan sudrash boshlanmaydi, aks holda
            pointer capture ularning bosilishini o'g'irlab qo'yardi. */}
        <div className={styles.controls} data-no-drag>
          <button
            type="button"
            className={styles.control}
            onClick={toggleExpanded}
            aria-label={isExpanded ? t('chat_collapse') : t('chat_expand_side')}
            title={isExpanded ? t('chat_collapse') : t('chat_expand_side')}
          >
            <Icon name={isExpanded ? 'collapse' : 'expand'} />
          </button>
          <button
            type="button"
            className={styles.control}
            onClick={close}
            aria-label={t('chat_close')}
            title={t('chat_close')}
          >
            <Icon name="close" />
          </button>
        </div>
      </header>

      <div className={styles.body}>
        {isExpanded && isDesktop && <ChatSessions />}

        <div className={styles.conversation}>
          {/* Yoyilgan holatda xabarlar juda kenglashib ketmasligi uchun
              o'rtaga tekislangan ustunga o'raladi (700px). */}
          <div className={styles.conversationInner}>
            <MessageList messages={messages} />
            <ChatComposer disabled={isBusy} onSubmit={(question) => ask(question)} />
            <p className={styles.disclaimer}>{t('disclaimer_short')}</p>
          </div>
        </div>
      </div>
    </section>
  )
}
