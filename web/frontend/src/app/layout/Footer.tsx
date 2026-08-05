import { Link } from 'react-router-dom'

import { useI18n } from '@shared/i18n'
import type { TranslationKey } from '@shared/i18n'
import { Icon } from '@shared/ui/Icon'

import { ROUTES } from '../routes'
import styles from './Footer.module.css'

interface FooterLink {
  to: string
  labelKey: TranslationKey
}

const COLUMNS: { titleKey: TranslationKey; items: FooterLink[] }[] = [
  {
    titleKey: 'footer_info',
    items: [
      { to: ROUTES.databases, labelKey: 'nav_databases' },
      { to: ROUTES.sources, labelKey: 'nav_sources' },
      { to: ROUTES.faq, labelKey: 'nav_faq' },
    ],
  },
  {
    titleKey: 'footer_users',
    items: [
      { to: ROUTES.categories, labelKey: 'nav_categories' },
      { to: ROUTES.services, labelKey: 'services_title' },
    ],
  },
  {
    titleKey: 'footer_contact_col',
    items: [{ to: ROUTES.contact, labelKey: 'nav_contact' }],
  },
]

export function Footer() {
  const { t } = useI18n()

  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <div className={styles.columns}>
          {COLUMNS.map((column) => (
            <div key={column.titleKey} className={styles.column}>
              <h4>{t(column.titleKey)}</h4>
              {column.items.map((item) => (
                <Link key={item.to} to={item.to} className={styles.item}>
                  {t(item.labelKey)}
                </Link>
              ))}
            </div>
          ))}
        </div>

        <div className={styles.bottom}>
          <span>{t('footer_disclaimer')}</span>
          <span className={styles.social} aria-hidden="true">
            <Icon name="telegram" />
          </span>
        </div>
      </div>
    </footer>
  )
}
