import { useI18n } from '@shared/i18n'
import type { TranslationKey } from '@shared/i18n'

import styles from './PromoSection.module.css'

const PROMOS: { titleKey: TranslationKey; textKey: TranslationKey }[] = [
  { titleKey: 'promo1_title', textKey: 'promo1_text' },
  { titleKey: 'promo2_title', textKey: 'promo2_text' },
]

export function PromoSection() {
  const { t } = useI18n()

  return (
    <div className={styles.row}>
      {PROMOS.map((promo) => (
        <article key={promo.titleKey} className={styles.card}>
          <h3 className={styles.title}>{t(promo.titleKey)}</h3>
          <p className={styles.text}>{t(promo.textKey)}</p>
        </article>
      ))}
    </div>
  )
}
