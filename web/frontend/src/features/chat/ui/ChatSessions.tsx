import { useMemo, useState } from 'react'

import { useI18n } from '@shared/i18n'
import { cx } from '@shared/lib/cx'
import { readStorage, writeStorage } from '@shared/lib/storage'
import { Icon } from '@shared/ui/Icon'

import { useChat } from '../model/useChat'
import styles from './ChatSessions.module.css'

const YIGILGAN_KALITI = 'compass:chat-sessions-rail'

/**
 * Yoyilgan chat ichidagi mini-panel: yangi suhbat, qidiruv va eski suhbatlar.
 * Sayt navbaridagi kabi ikonka-tugma bilan tor tasmaga yig'iladi/yoyiladi.
 */
export function ChatSessions() {
  const { t } = useI18n()
  const { chats, activeId, newChat, selectChat, deleteChat } = useChat()
  const [qidiruv, setQidiruv] = useState('')
  const [yigilgan, setYigilgan] = useState(() => readStorage(YIGILGAN_KALITI) === '1')

  const almashtirish = () => {
    setYigilgan((qiymat) => {
      const yangi = !qiymat
      writeStorage(YIGILGAN_KALITI, yangi ? '1' : '0')
      return yangi
    })
  }

  const royxat = useMemo(() => {
    const kalit = qidiruv.trim().toLowerCase()
    // Hali bitta ham savol yozilmagan bo'sh suhbat ro'yxatda ko'rinmaydi —
    // faqat haqiqiy (kamida bitta xabari bor) suhbatlar tarixga chiqadi.
    const bor = chats.filter((chat) => chat.xabarlar.length > 0)
    if (!kalit) return bor
    return bor.filter(
      (chat) =>
        chat.sarlavha.toLowerCase().includes(kalit) ||
        chat.xabarlar.some((x) => x.text.toLowerCase().includes(kalit)),
    )
  }, [chats, activeId, qidiruv])

  return (
    <aside className={cx(styles.panel, yigilgan && styles.rail)}>
      <div className={styles.top}>
        {!yigilgan && <span className={styles.topLabel}>{t('chat_history')}</span>}
        <button
          type="button"
          className={styles.toggle}
          onClick={almashtirish}
          aria-label={t('nav_toggle')}
          title={t('nav_toggle')}
        >
          <Icon name="panel" />
        </button>
      </div>

      <button
        type="button"
        className={styles.newChat}
        onClick={newChat}
        title={t('chat_new')}
      >
        <Icon name="plus" />
        {!yigilgan && t('chat_new')}
      </button>

      {!yigilgan && (
        <>
          <div className={styles.searchBox}>
            <Icon name="search" />
            <input
              className={styles.search}
              value={qidiruv}
              onChange={(event) => setQidiruv(event.target.value)}
              placeholder={t('chat_search')}
              aria-label={t('chat_search')}
              type="search"
            />
          </div>

          <div className={styles.list}>
            {royxat.length === 0 ? (
              <p className={styles.empty}>{t('chat_no_history')}</p>
            ) : (
              royxat.map((chat) => (
                <div
                  key={chat.id}
                  className={cx(styles.item, chat.id === activeId && styles.active)}
                >
                  <button
                    type="button"
                    className={styles.itemButton}
                    onClick={() => selectChat(chat.id)}
                    title={chat.sarlavha || t('chat_new')}
                  >
                    {chat.sarlavha || t('chat_new')}
                  </button>
                  <button
                    type="button"
                    className={styles.remove}
                    onClick={() => deleteChat(chat.id)}
                    aria-label={t('chat_delete')}
                    title={t('chat_delete')}
                  >
                    <Icon name="trash" />
                  </button>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </aside>
  )
}
