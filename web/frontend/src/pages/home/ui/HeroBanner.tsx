import { useChat } from '@features/chat'
import { useI18n } from '@shared/i18n'

import styles from './HeroBanner.module.css'

export function HeroBanner() {
  const { t } = useI18n()
  const { open } = useChat()

  return (
    <section className={styles.banner}>
      <div className={styles.copy}>
        <h1 className={styles.title}>{t('banner_title')}</h1>
        <p className={styles.text}>{t('banner_text')}</p>
      </div>
      <button type="button" className={styles.cta} onClick={open}>
        {t('open_chat')}
      </button>
    </section>
  )
}
