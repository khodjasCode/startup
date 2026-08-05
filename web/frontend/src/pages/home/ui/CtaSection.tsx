import { useChat } from '@features/chat'
import { useI18n } from '@shared/i18n'

import styles from './CtaSection.module.css'

export function CtaSection() {
  const { t } = useI18n()
  const { open } = useChat()

  return (
    <section className={styles.cta}>
      <h2 className={styles.title}>{t('cta_title')}</h2>
      <p className={styles.text}>{t('cta_text')}</p>
      <button type="button" className={styles.button} onClick={open}>
        {t('open_chat')}
      </button>
    </section>
  )
}
