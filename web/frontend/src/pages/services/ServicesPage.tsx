import { useCallback, useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'

import { ServiceList, fetchSohalar, fetchXizmatlar } from '@features/catalog'
import { useI18n } from '@shared/i18n'
import { cx } from '@shared/lib/cx'
import { dataLabel } from '@shared/lib/dataLabels'
import { useAsync } from '@shared/lib/useAsync'
import { useDebounced } from '@shared/lib/useDebounced'
import { Empty, Loading, LoadError } from '@shared/ui/AsyncState'
import { Icon } from '@shared/ui/Icon'

import styles from './ServicesPage.module.css'

const SAHIFA = 20

/**
 * Katalog: chapda yo'nalishlar ro'yxati (o'z scroll'i bilan), o'ngda tanlangan
 * yo'nalish yozuvlari. Tanlov URL'da saqlanadi (?soha=...&q=...), shuning uchun
 * havolani ulashish yoki sahifani yangilash mumkin.
 */
export function ServicesPage() {
  const { t, locale } = useI18n()
  const [params, setParams] = useSearchParams()

  const soha = params.get('soha') ?? ''
  const qFromUrl = params.get('q') ?? ''

  const [qInput, setQInput] = useState(qFromUrl)
  const q = useDebounced(qInput, 300)
  const [limit, setLimit] = useState(SAHIFA)

  // Qidiruv matni to'xtaganda URL'ni yangilaymiz (tarixni to'ldirmasdan).
  useEffect(() => {
    const joriy = params.get('q') ?? ''
    if (joriy === q) return
    const yangi = new URLSearchParams(params)
    if (q) yangi.set('q', q)
    else yangi.delete('q')
    setParams(yangi, { replace: true })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q])

  useEffect(() => setLimit(SAHIFA), [soha, q])

  const fetcher = useCallback(
    (signal: AbortSignal) => fetchXizmatlar({ soha, q, limit }, signal),
    [soha, q, limit],
  )
  const { data, loading, error } = useAsync(fetcher, [soha, q, limit])

  const sohalarFetcher = useCallback((signal: AbortSignal) => fetchSohalar(signal), [])
  const sohalar = useAsync(sohalarFetcher, [])

  const sohaniOrnat = (yangiSoha: string) => {
    const yangi = new URLSearchParams(params)
    if (yangiSoha) yangi.set('soha', yangiSoha)
    else yangi.delete('soha')
    setParams(yangi)
  }

  return (
    <main className={styles.page}>
      {/* Chapdagi yo'nalishlar ustuni — sahifa bilan birga emas, o'zi aylanadi. */}
      <aside className={styles.rail}>
        <h2 className={styles.railTitle}>{t('category_list')}</h2>
        <nav className={styles.railList}>
          <button
            type="button"
            className={cx(styles.railItem, !soha && styles.railItemActive)}
            onClick={() => sohaniOrnat('')}
          >
            <span>{t('category_all')}</span>
          </button>

          {(sohalar.data ?? []).map((item) => (
            <button
              key={item.nomi}
              type="button"
              className={cx(styles.railItem, soha === item.nomi && styles.railItemActive)}
              onClick={() => sohaniOrnat(item.nomi)}
            >
              <span>{dataLabel(item.nomi, locale)}</span>
              <b className={styles.railCount}>{item.soni}</b>
            </button>
          ))}
        </nav>
      </aside>

      <section className={styles.content}>
        <header className={styles.head}>
          <h1 className={styles.title}>{soha ? dataLabel(soha, locale) : t('services_title')}</h1>
          <div className={styles.searchBox}>
            <Icon name="search" />
            <input
              className={styles.search}
              value={qInput}
              onChange={(event) => setQInput(event.target.value)}
              placeholder={t('services_search')}
              aria-label={t('services_search')}
              type="search"
            />
          </div>
        </header>

        {loading && !data && <Loading />}
        {error && <LoadError />}

        {data && (
          <>
            <p className={styles.count}>
              {t('services_found')}: {data.jami}
            </p>

            {data.xizmatlar.length === 0 ? (
              <Empty text={t('category_empty')} />
            ) : (
              <>
                <ServiceList items={data.xizmatlar} />
                {data.jami > data.xizmatlar.length && (
                  <button
                    type="button"
                    className={styles.more}
                    onClick={() => setLimit((value) => value + SAHIFA)}
                    disabled={loading}
                  >
                    {t('faq_more')}
                  </button>
                )}
              </>
            )}
          </>
        )}
      </section>
    </main>
  )
}
