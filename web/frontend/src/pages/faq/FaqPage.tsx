import { useCallback, useEffect, useState } from 'react'

import { fetchSavolJavob } from '@features/catalog'
import { useI18n } from '@shared/i18n'
import { cx } from '@shared/lib/cx'
import { dataLabel } from '@shared/lib/dataLabels'
import { useAsync } from '@shared/lib/useAsync'
import { useDebounced } from '@shared/lib/useDebounced'
import { Empty, Loading, LoadError } from '@shared/ui/AsyncState'
import { Icon } from '@shared/ui/Icon'
import { Page } from '@shared/ui/Page'

import styles from './FaqPage.module.css'

/**
 * Savol-javob: mavzu bloklari, ichida shu sohaga oid savollar (my.gov.uz/faq
 * uslubida). Qidiruvda mos savollar bor bloklar avtomatik ochiladi.
 */
export function FaqPage() {
  const { t, locale } = useI18n()
  const [qInput, setQInput] = useState('')
  const q = useDebounced(qInput, 300)
  const [ochiq, setOchiq] = useState<string | null>(null)

  const fetcher = useCallback((signal: AbortSignal) => fetchSavolJavob({ q }, signal), [q])
  const { data, loading, error } = useAsync(fetcher, [q])

  // Qidiruv paytida birinchi blok ochiq turadi — natija darhol ko'rinsin.
  useEffect(() => {
    if (q && data?.guruhlar.length) setOchiq(data.guruhlar[0]?.nomi ?? null)
    if (!q) setOchiq(null)
  }, [q, data])

  return (
    <Page title={t('faq_title')} subtitle={t('faq_subtitle')}>
      <input
        className={styles.search}
        value={qInput}
        onChange={(event) => setQInput(event.target.value)}
        placeholder={t('faq_search')}
        aria-label={t('faq_search')}
        type="search"
      />

      {loading && !data && <Loading />}
      {error && <LoadError />}

      {data &&
        (data.guruhlar.length === 0 ? (
          <Empty />
        ) : (
          <div className={styles.groups}>
            {data.guruhlar.map((guruh) => {
              const ochiqmi = ochiq === guruh.nomi
              return (
                <section key={guruh.nomi} className={cx(styles.group, ochiqmi && styles.groupOpen)}>
                  <button
                    type="button"
                    className={styles.groupHead}
                    onClick={() => setOchiq(ochiqmi ? null : guruh.nomi)}
                    aria-expanded={ochiqmi}
                  >
                    <span className={styles.groupName}>{dataLabel(guruh.nomi, locale)}</span>
                    <span className={styles.count}>{guruh.soni}</span>
                    <Icon name="chevronDown" className={styles.chevron} />
                  </button>

                  {ochiqmi && (
                    <div className={styles.questions}>
                      {guruh.savollar.map((item) => (
                        <details key={item.id} className={styles.item}>
                          <summary className={styles.question}>{item.savol}</summary>
                          <div className={styles.answer}>
                            {item.javob && <p className={styles.text}>{item.javob}</p>}
                            {item.izoh && <p className={styles.note}>{item.izoh}</p>}
                            {item.url && (
                              <a
                                className={styles.link}
                                href={item.url}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                {t('service_open_source')}
                              </a>
                            )}
                          </div>
                        </details>
                      ))}
                    </div>
                  )}
                </section>
              )
            })}
          </div>
        ))}
    </Page>
  )
}
