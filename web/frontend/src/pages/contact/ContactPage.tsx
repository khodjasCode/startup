import { useCallback } from 'react'
import { Link } from 'react-router-dom'

import { ROUTES } from '@app/routes'
import { useChat } from '@features/chat'
import { fetchManbalar } from '@features/catalog'
import { useI18n } from '@shared/i18n'
import { useAsync } from '@shared/lib/useAsync'
import { Loading, LoadError } from '@shared/ui/AsyncState'
import { Icon } from '@shared/ui/Icon'
import { Page } from '@shared/ui/Page'

import styles from './ContactPage.module.css'

/** Matndan qisqa raqamlarni ajratib oladi: "1242 (portal bo'yicha)" → "1242". */
function raqamlarniTopish(matn: string): string[] {
  return [...new Set(matn.match(/(?:\+?\d[\d\-\s]{2,}\d)/g) ?? [])]
    .map((r) => r.trim())
    .filter((r) => r.replace(/\D/g, '').length >= 3)
    .slice(0, 2)
}

/**
 * Aloqa sahifasi: rasmiy kanallar bazadan olinadi (qo'lda yozilgan raqamlar
 * eskirmasligi uchun). Ixcham kartochkalar tarmog'i — telefon raqami markazda
 * ko'zga tashlanadi, uzun "aloqa" matni takrorlanmaydi.
 */
export function ContactPage() {
  const { t } = useI18n()
  const { open } = useChat()
  const fetcher = useCallback((signal: AbortSignal) => fetchManbalar(signal), [])
  const { data, loading, error } = useAsync(fetcher, [])

  const aloqali = (data ?? []).filter((manba) => manba.aloqa)

  return (
    <Page title={t('contact_title')} subtitle={t('contact_subtitle')}>
      {/* Tezkor yo'llar — bir xil uslubdagi uchta katta harakat. */}
      <div className={styles.quick}>
        <button type="button" className={styles.quickItem} onClick={open}>
          <Icon name="badge" />
          <span className={styles.quickText}>
            <b>{t('open_chat')}</b>
            <small>{t('banner_text')}</small>
          </span>
          <Icon name="arrowRight" className={styles.quickArrow} />
        </button>

        <Link to={ROUTES.faq} className={styles.quickItem}>
          <Icon name="question" />
          <span className={styles.quickText}>
            <b>{t('nav_faq')}</b>
            <small>{t('faq_subtitle')}</small>
          </span>
          <Icon name="arrowRight" className={styles.quickArrow} />
        </Link>

        <Link to={ROUTES.sources} className={styles.quickItem}>
          <Icon name="link" />
          <span className={styles.quickText}>
            <b>{t('nav_sources')}</b>
            <small>{t('sources_subtitle')}</small>
          </span>
          <Icon name="arrowRight" className={styles.quickArrow} />
        </Link>
      </div>

      <h2 className={styles.sectionTitle}>{t('contact_official')}</h2>
      {loading && <Loading />}
      {error && <LoadError />}

      <div className={styles.grid}>
        {aloqali.map((manba) => {
          const raqamlar = raqamlarniTopish(manba.aloqa)
          return (
            <article key={manba.kalit} className={styles.card}>
              <h3 className={styles.name}>{manba.nomi}</h3>

              {raqamlar.length > 0 ? (
                <div className={styles.phones}>
                  {raqamlar.map((raqam) => (
                    <a
                      key={raqam}
                      href={`tel:${raqam.replace(/[^\d+]/g, '')}`}
                      className={styles.phone}
                    >
                      <Icon name="phone" />
                      {raqam}
                    </a>
                  ))}
                </div>
              ) : (
                <p className={styles.detail}>{manba.aloqa}</p>
              )}

              {manba.url && (
                <a
                  className={styles.site}
                  href={manba.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {manba.url.replace(/^https?:\/\//, '').replace(/\/$/, '')}
                  <Icon name="arrowRight" />
                </a>
              )}
            </article>
          )
        })}
      </div>

      <p className={styles.note}>{t('disclaimer_short')}</p>
    </Page>
  )
}
