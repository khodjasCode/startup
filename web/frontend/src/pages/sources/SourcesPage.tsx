import { useCallback } from 'react'

import { fetchManbalar } from '@features/catalog'
import { useI18n } from '@shared/i18n'
import { localizeManba } from '@shared/lib/localizeContent'
import { useAsync } from '@shared/lib/useAsync'
import { Loading, LoadError } from '@shared/ui/AsyncState'
import { Icon } from '@shared/ui/Icon'
import { Page } from '@shared/ui/Page'

import styles from './SourcesPage.module.css'

/**
 * Manbalar: har biri ixcham kartochka — nom, qisqa tavsif, aloqa va havola
 * doim ko'rinadi; kirish tartibi (uzun bosqichlar ro'yxati) esa bosilganda
 * ochiladi, aks holda sahifa haddan tashqari uzun bo'lib ketardi.
 */
export function SourcesPage() {
  const { t, locale } = useI18n()
  const fetcher = useCallback((signal: AbortSignal) => fetchManbalar(signal), [])
  const { data, loading, error } = useAsync(fetcher, [])

  return (
    <Page title={t('sources_title')} subtitle={t('sources_subtitle')}>
      {loading && <Loading />}
      {error && <LoadError />}

      <div className={styles.grid}>
        {(data ?? []).map((xom) => {
          const manba = localizeManba(xom, locale)
          return (
          <article key={manba.kalit} className={styles.card}>
            <h2 className={styles.title}>{manba.nomi}</h2>
            {manba.tavsif && <p className={styles.text}>{manba.tavsif}</p>}

            {manba.aloqa && (
              <p className={styles.contact}>
                <strong>{t('sources_contact')}:</strong> {manba.aloqa}
              </p>
            )}

            {manba.kirish_tartibi.length > 0 && (
              <details className={styles.details}>
                <summary className={styles.summary}>
                  {t('sources_login_order')}
                  <Icon name="chevronDown" className={styles.chevron} />
                </summary>
                <ol className={styles.steps}>
                  {manba.kirish_tartibi.map((qadam, index) => (
                    <li key={index}>{qadam}</li>
                  ))}
                </ol>
              </details>
            )}

            <footer className={styles.foot}>
              <span className={styles.count}>
                {manba.xizmatlar_soni} {t('records_count')}
              </span>
              {manba.url && (
                <a
                  className={styles.link}
                  href={manba.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {t('sources_open')}
                  <Icon name="arrowRight" />
                </a>
              )}
            </footer>
          </article>
          )
        })}
      </div>
    </Page>
  )
}
