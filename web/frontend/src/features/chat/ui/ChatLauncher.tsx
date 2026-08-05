import { useI18n } from '@shared/i18n'

import { useChat } from '../model/useChat'
import styles from './ChatLauncher.module.css'

/** Pastki-o'ng burchakdagi doimiy tugma: chat panelini ochadi/yopadi. */
export function ChatLauncher() {
  const { t } = useI18n()
  const { isOpen, toggle } = useChat()

  // Chat ochiq bo'lganda (oyna yoki yoyilgan — farqi yo'q) tugma yashiriladi —
  // aks holda pastki-o'ng burchakda panel bilan ustma-ust tushib qolardi.
  // Chat yopilganda tugma joyiga qaytadi.
  if (isOpen) return null

  return (
    <button
      type="button"
      className={styles.launcher}
      onClick={toggle}
      aria-expanded={isOpen}
      aria-label={isOpen ? t('chat_close') : t('chat_open')}
    >
      <img src="/images/ai-logo.png" alt="" />
    </button>
  )
}
