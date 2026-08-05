import { useI18n } from '@shared/i18n'
import { useTheme } from '@shared/theme'
import { Icon } from '@shared/ui/Icon'

import styles from './ThemeToggle.module.css'

/**
 * Mavzu almashtirgich: quyosh ↔ oy. Ikonka joriy holatni emas, bosilganda nima
 * bo'lishini ko'rsatadi (qorong'ida — quyosh, yorug'da — oy).
 */
export function ThemeToggle() {
  const { t } = useI18n()
  const { resolved, setChoice } = useTheme()

  const keyingisi = resolved === 'dark' ? 'light' : 'dark'
  const yorliq = keyingisi === 'dark' ? t('theme_to_dark') : t('theme_to_light')

  return (
    <button
      type="button"
      className={styles.button}
      onClick={() => setChoice(keyingisi)}
      aria-label={yorliq}
      title={yorliq}
    >
      <Icon name={keyingisi === 'dark' ? 'moon' : 'sun'} />
    </button>
  )
}
