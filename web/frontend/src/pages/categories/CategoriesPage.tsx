import { useCallback } from 'react'
import { Link } from 'react-router-dom'

import { fetchSohalar } from '@features/catalog'
import { useI18n } from '@shared/i18n'
import { dataLabel } from '@shared/lib/dataLabels'
import { useAsync } from '@shared/lib/useAsync'
import { Empty, Loading, LoadError } from '@shared/ui/AsyncState'
import { Page } from '@shared/ui/Page'

import styles from './CategoriesPage.module.css'

export function CategoriesPage() {
  const { t, locale } = useI18n()
  const fetcher = useCallback((signal: AbortSignal) => fetchSohalar(signal), [])
  const { data, loading, error } = useAsync(fetcher, [])

  return (
    <Page title={t('categories_title')} subtitle={t('categories_subtitle')}>
      {loading && <Loading />}
      {error && <LoadError />}
      {data && data.length === 0 && <Empty />}
      {data && data.length > 0 && (
        <div className={styles.grid}>
          {data.map((soha) => (
            <Link
              key={soha.nomi}
              // Havolada — bazadagi asl (o'zbekcha) nom: backend shu bo'yicha filtrlaydi.
              to={`/xizmatlar?soha=${encodeURIComponent(soha.nomi)}`}
              className={styles.card}
            >
              <h2 className={styles.name}>{dataLabel(soha.nomi, locale)}</h2>
              <span className={styles.count}>
                {soha.soni} {t('records_count')}
              </span>
            </Link>
          ))}
        </div>
      )}
    </Page>
  )
}
