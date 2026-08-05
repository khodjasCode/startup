import { useCallback, useRef, useState } from 'react'

import { LOCALES, LOCALE_LABELS, useI18n } from '@shared/i18n'
import { cx } from '@shared/lib/cx'
import { useOnClickOutside } from '@shared/lib/useOnClickOutside'
import { Flag } from '@shared/ui/Flag'
import { Icon } from '@shared/ui/Icon'

import styles from './LanguageSwitcher.module.css'

/**
 * Til tanlash: ochiladigan menyu. Tugmada ham, ro'yxatda ham faqat bayroq va
 * qisqa kod (UZB / RU / EN) — uzun nomlarsiz.
 */
export function LanguageSwitcher() {
  const { locale, setLocale, t } = useI18n()
  const [ochiq, setOchiq] = useState(false)
  const wrapRef = useRef<HTMLDivElement>(null)

  useOnClickOutside(
    wrapRef,
    useCallback(() => setOchiq(false), []),
    ochiq,
  )

  return (
    <div ref={wrapRef} className={styles.wrap}>
      <button
        type="button"
        className={styles.trigger}
        onClick={() => setOchiq((qiymat) => !qiymat)}
        aria-haspopup="menu"
        aria-expanded={ochiq}
        aria-label={t('language')}
        title={LOCALE_LABELS[locale].full}
      >
        <Flag locale={locale} className={styles.flag} />
        <span className={styles.code}>{LOCALE_LABELS[locale].short}</span>
        <Icon name="chevronDown" className={cx(styles.chevron, ochiq && styles.chevronOpen)} />
      </button>

      {ochiq && (
        <div className={styles.menu} role="menu">
          {LOCALES.map((item) => (
            <button
              key={item}
              type="button"
              role="menuitemradio"
              aria-checked={item === locale}
              className={cx(styles.option, item === locale && styles.active)}
              onClick={() => {
                setLocale(item)
                setOchiq(false)
              }}
              title={LOCALE_LABELS[item].full}
            >
              <Flag locale={item} className={styles.flag} />
              <span className={styles.code}>{LOCALE_LABELS[item].short}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
