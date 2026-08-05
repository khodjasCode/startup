import { useI18n } from '@shared/i18n'

import styles from './AsyncState.module.css'

/** Yuklanmoqda / xatolik / bo'sh natija — uch holat uchun yagona ko'rinish. */
export function Loading() {
  const { t } = useI18n()
  return (
    <div className={styles.state} role="status">
      <span className={styles.spinner} aria-hidden="true" />
      {t('state_loading')}
    </div>
  )
}

export function LoadError({ onRetry }: { onRetry?: () => void }) {
  const { t } = useI18n()
  return (
    <div className={`${styles.state} ${styles.error}`}>
      {t('state_error')}
      {onRetry && (
        <button type="button" className={styles.retry} onClick={onRetry}>
          {t('state_retry')}
        </button>
      )}
    </div>
  )
}

export function Empty({ text }: { text?: string }) {
  const { t } = useI18n()
  return <div className={styles.state}>{text ?? t('state_empty')}</div>
}
