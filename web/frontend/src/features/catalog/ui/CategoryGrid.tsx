import { useCallback } from 'react'
import { Link } from 'react-router-dom'

import { useI18n } from '@shared/i18n'
import { dataLabel } from '@shared/lib/dataLabels'
import { useAsync } from '@shared/lib/useAsync'
import { Loading, LoadError } from '@shared/ui/AsyncState'
import { Icon } from '@shared/ui/Icon'

import { fetchSohalar } from '../api/katalogApi'
import styles from './CategoryGrid.module.css'

interface CategoryGridProps {
  /** Nechta yo'nalish ko'rsatilsin (bosh sahifada — qisqartirilgan ro'yxat). */
  limit?: number
}

/**
 * Yo'nalishlar ro'yxati — bazadagi haqiqiy sohalardan quriladi (qo'lda yozilgan
 * kartochkalar emas). Bosilganda shu yo'nalish katalogi ochiladi.
 */
export function CategoryGrid({ limit }: CategoryGridProps) {
  const { t, locale } = useI18n()
  const fetcher = useCallback((signal: AbortSignal) => fetchSohalar(signal), [])
  const { data, loading, error } = useAsync(fetcher, [])

  if (loading && !data) return <Loading />
  if (error) return <LoadError />

  const sohalar = limit ? (data ?? []).slice(0, limit) : (data ?? [])

  return (
    <ul className={styles.list}>
      {sohalar.map((soha) => (
        <li key={soha.nomi}>
          <Link to={`/xizmatlar?soha=${encodeURIComponent(soha.nomi)}`} className={styles.item}>
            <span className={styles.name}>{dataLabel(soha.nomi, locale)}</span>
            <span className={styles.count}>
              {soha.soni} {t('records_count')}
            </span>
            <Icon name="arrowRight" className={styles.arrow} />
          </Link>
        </li>
      ))}
    </ul>
  )
}
