import { useAuth } from '@features/auth'
import { useI18n } from '@shared/i18n'
import { cx } from '@shared/lib/cx'
import { DEFAULT_REGION, regionNomi } from '@shared/lib/regions'

import { useServerClock } from '../model/useServerClock'
import styles from './Clock.module.css'

const ikkiXona = (son: number) => String(son).padStart(2, '0')

/**
 * Sarlavhadagi soat: soat:daqiqa lipillovchi ikki nuqta bilan + soniya.
 *
 * Butun O'zbekiston bitta vaqt mintaqasida (UTC+5, yozgi vaqtsiz), shuning
 * uchun hudud tanlovi vaqtning o'zini emas — faqat ostidagi shahar/viloyat
 * yorlig'ini o'zgartiradi. Kirmagan yoki hudud tanlamagan foydalanuvchi uchun
 * standart — Toshkent.
 */
export function Clock() {
  const { t, locale } = useI18n()
  const { user } = useAuth()
  const { soat, daqiqa, soniya, ulangan } = useServerClock()

  const hududNomi = regionNomi(user?.hudud || DEFAULT_REGION, locale) || t('clock_tashkent')

  return (
    <div
      className={styles.clock}
      title={ulangan ? t('clock_live') : t('clock_local')}
      aria-label={`${hududNomi} ${ikkiXona(soat)}:${ikkiXona(daqiqa)}`}
    >
      <span className={styles.city}>
        <span className={cx(styles.dot, ulangan && styles.dotLive)} aria-hidden="true" />
        {hududNomi}
      </span>
      <span className={styles.time}>
        {ikkiXona(soat)}
        <span className={styles.colon}>:</span>
        {ikkiXona(daqiqa)}
        <span className={styles.seconds}>{ikkiXona(soniya)}</span>
      </span>
    </div>
  )
}
