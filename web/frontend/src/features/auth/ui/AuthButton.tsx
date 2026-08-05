import { useCallback, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import { useI18n } from '@shared/i18n'
import { useOnClickOutside } from '@shared/lib/useOnClickOutside'
import { Icon } from '@shared/ui/Icon'

import { useAuth } from '../model/useAuth'
import styles from './AuthButton.module.css'

/** Sarlavhadagi "Kirish" havolasi yoki (kirgan bo'lsa) foydalanuvchi menyusi. */
export function AuthButton() {
  const { t } = useI18n()
  const { user, loading, logout } = useAuth()

  const [menyuOchiq, setMenyuOchiq] = useState(false)
  const wrapRef = useRef<HTMLDivElement>(null)

  useOnClickOutside(
    wrapRef,
    useCallback(() => setMenyuOchiq(false), []),
    menyuOchiq,
  )

  if (loading) {
    return <span className={styles.placeholder} aria-hidden="true" />
  }

  if (!user) {
    return (
      <Link to="/kirish" className={styles.login}>
        {t('auth_login')}
      </Link>
    )
  }

  return (
    <div ref={wrapRef} className={styles.wrap}>
      <button
        type="button"
        className={styles.user}
        onClick={() => setMenyuOchiq((value) => !value)}
        aria-haspopup="menu"
        aria-expanded={menyuOchiq}
        aria-label={t('auth_account')}
      >
        <span className={styles.avatar}>
          <Icon name="user" />
        </span>
        <span className={styles.name}>{user.telefon_korinishi}</span>
        <Icon name="chevronDown" className={styles.chevron} />
      </button>

      {menyuOchiq && (
        <div className={styles.menu} role="menu">
          <div className={styles.meta}>{user.telefon_korinishi}</div>
          <button
            type="button"
            role="menuitem"
            className={styles.logout}
            onClick={() => {
              setMenyuOchiq(false)
              void logout()
            }}
          >
            {t('auth_logout')}
          </button>
        </div>
      )}
    </div>
  )
}
