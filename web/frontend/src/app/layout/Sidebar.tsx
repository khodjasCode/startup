import { NavLink } from 'react-router-dom'

import { useI18n } from '@shared/i18n'
import { cx } from '@shared/lib/cx'
import { useTheme } from '@shared/theme'
import { Icon } from '@shared/ui/Icon'

import { NAV_SECTIONS, ROUTES } from '../routes'
import styles from './Sidebar.module.css'

interface SidebarProps {
  /** Yoyilgan holatmi (yozuvlar bilan) yoki tor tasmami (faqat ikonkalar). */
  isOpen: boolean
  /** Kichik ekranda panel kontent ustidan chiqadi — havola bosilsa yopiladi. */
  onClose: () => void
  onToggle: () => void
}

export function Sidebar({ isOpen, onClose, onToggle }: SidebarProps) {
  const { t } = useI18n()
  const { resolved } = useTheme()

  // Qorong'i mavzuda oq chizmali belgi ishlatiladi; yorug'da — rangli.
  const qorongi = resolved === 'dark'
  const yigilgan = !isOpen

  return (
    <>
      {isOpen && <div className={styles.backdrop} onClick={onClose} />}

      <aside className={cx(styles.sidebar, yigilgan && styles.rail)}>
        {/* Yig'ilgan holatda yig'ish tugmasi ko'rinmaydi; logotip ustiga
            kursor kelganda uning o'rnida yoyish tugmasi paydo bo'ladi. */}
        <div className={styles.top}>
          <NavLink to={ROUTES.home} className={cx(styles.brand)} onClick={onClose}>
            <img
              src={qorongi ? '/images/logo-mark-dark.png' : '/images/logo-mark-light.png'}
              alt=""
              className={styles.logo}
            />
            <span className={styles.brandName}>Compass</span>
          </NavLink>

          <button
            type="button"
            className={styles.toggle}
            onClick={onToggle}
            aria-label={t('nav_toggle')}
            title={t('nav_toggle')}
          >
            <Icon name="panel" />
          </button>
        </div>

        {NAV_SECTIONS.map((section) => (
          <nav key={section.titleKey} className={styles.section}>
            <div className={styles.sectionTitle}>{t(section.titleKey)}</div>
            {section.items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === ROUTES.home}
                onClick={onClose}
                title={t(item.labelKey)}
                className={({ isActive }) => cx(styles.item, isActive && styles.itemActive)}
              >
                <Icon name={item.icon} />
                <span className={styles.label}>{t(item.labelKey)}</span>
              </NavLink>
            ))}
          </nav>
        ))}

        <p className={styles.foot}>{t('disclaimer_short')}</p>
      </aside>
    </>
  )
}
