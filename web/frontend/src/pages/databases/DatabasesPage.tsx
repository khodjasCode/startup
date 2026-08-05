import { useCallback } from 'react'

import { fetchStatistika } from '@features/catalog'
import { useI18n } from '@shared/i18n'
import { useAsync } from '@shared/lib/useAsync'
import { Loading, LoadError } from '@shared/ui/AsyncState'
import { Page } from '@shared/ui/Page'

import styles from './DatabasesPage.module.css'

export function DatabasesPage() {
  const { t } = useI18n()
  const fetcher = useCallback((signal: AbortSignal) => fetchStatistika(signal), [])
  const { data, loading, error } = useAsync(fetcher, [])

  return (
    <Page title={t('databases_title')} subtitle={t('databases_subtitle')}>
      {loading && <Loading />}
      {error && <LoadError />}

      {data && (
        <>
          <div className={styles.stats}>
            <div className={styles.stat}>
              <span className={styles.value}>{data.jami_yozuvlar}</span>
              <span className={styles.label}>{t('databases_total')}</span>
            </div>
            <div className={styles.stat}>
              <span className={styles.value}>{data.sohalar_soni}</span>
              <span className={styles.label}>{t('databases_areas')}</span>
            </div>
            <div className={styles.stat}>
              <span className={styles.value}>{data.faq_soni}</span>
              <span className={styles.label}>{t('databases_faq')}</span>
            </div>
          </div>

          <ul className={styles.list}>
            {data.manbalar.map((manba) => (
              <li key={manba.kalit} className={styles.item}>
                <div className={styles.itemMain}>
                  <h2 className={styles.itemTitle}>{manba.nomi}</h2>
                  {manba.tavsif && <p className={styles.itemText}>{manba.tavsif}</p>}
                  {manba.yigilgan_sana && (
                    <p className={styles.meta}>
                      {t('databases_collected')}: {manba.yigilgan_sana}
                    </p>
                  )}
                </div>
                <span className={styles.badge}>
                  {manba.xizmatlar_soni} {t('records_count')}
                </span>
              </li>
            ))}
          </ul>
        </>
      )}
    </Page>
  )
}
