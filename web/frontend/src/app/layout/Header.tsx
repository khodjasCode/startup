import { useNavigate } from 'react-router-dom'

import { AuthButton } from '@features/auth'
import { Clock } from '@features/clock'
import { LanguageSwitcher } from '@features/language-switcher'
import { ThemeToggle } from '@features/theme-toggle'
import { useI18n } from '@shared/i18n'
import { Icon } from '@shared/ui/Icon'

import { ROUTES } from '../routes'
import styles from './Header.module.css'

interface HeaderProps {
  onToggleSidebar: () => void
  sidebarOpen: boolean
}

export function Header({ onToggleSidebar, sidebarOpen }: HeaderProps) {
  const { t } = useI18n()
  const navigate = useNavigate()

  return (
    <header className={styles.header}>
      {/* Yagona ikonka-tugma: yon panelni ochadi va yopadi (yozuvsiz, ataylab). */}
      <button
        type="button"
        className={styles.toggle}
        onClick={onToggleSidebar}
        aria-label={t('nav_toggle')}
        aria-expanded={sidebarOpen}
        title={t('nav_toggle')}
      >
        <Icon name="menu" />
      </button>

      {/* Qidiruv: xizmatlar katalogiga o'tkazadi (RAG chat alohida tugmada). */}
      <button type="button" className={styles.search} onClick={() => navigate(ROUTES.services)}>
        <Icon name="search" />
        <span className={styles.searchText}>{t('services_search')}</span>
      </button>

      <div className={styles.spacer} />

      <div className={styles.actions}>
        <Clock />
        <LanguageSwitcher />
        <ThemeToggle />
        <AuthButton />
      </div>
    </header>
  )
}
