import { useCallback, useMemo } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { useChat } from '@features/chat'
import { fetchXizmat } from '@features/catalog'
import { useI18n } from '@shared/i18n'
import type { TranslationKey } from '@shared/i18n'
import { dataLabel } from '@shared/lib/dataLabels'
import { localizeXizmat } from '@shared/lib/localizeContent'
import { useAsync } from '@shared/lib/useAsync'
import { Loading, LoadError } from '@shared/ui/AsyncState'
import { Icon } from '@shared/ui/Icon'
import { Page } from '@shared/ui/Page'

import styles from './ServicePage.module.css'

function Bolim({ sarlavha, children }: { sarlavha: string; children: React.ReactNode }) {
  return (
    <section className={styles.section}>
      <h2 className={styles.sectionTitle}>{sarlavha}</h2>
      {children}
    </section>
  )
}

export function ServicePage() {
  const { t, locale } = useI18n()
  const { id = '' } = useParams()
  const { open, ask } = useChat()
  const navigate = useNavigate()

  const fetcher = useCallback((signal: AbortSignal) => fetchXizmat(id, signal), [id])
  const { data: xom, loading, error } = useAsync(fetcher, [id])
  // Ru/en tanlanganda backend tayyorlagan tarjima ko'rsatiladi (bo'lsa).
  const data = useMemo(() => (xom ? localizeXizmat(xom, locale) : null), [xom, locale])

  // Qaysi yo'ldan kelgan bo'lsa (kategoriya, qidiruv, chat) — o'sha yerga
  // qaytaradi; tarix bo'lmasa (havola to'g'ridan-to'g'ri ochilgan bo'lsa)
  // kategoriyalar ro'yxatiga tushadi.
  const orqagaQaytish = () => {
    if (window.history.length > 1) navigate(-1)
    else navigate('/kategoriyalar')
  }

  const OrqagaTugmasi = (
    <button type="button" onClick={orqagaQaytish} className={styles.back}>
      <Icon name="arrowRight" className={styles.backIcon} />
      {t('back')}
    </button>
  )

  if (loading) {
    return (
      <Page title="…">
        <Loading />
      </Page>
    )
  }
  if (error || !data) {
    return (
      <Page title={t('state_error')}>
        <LoadError />
        {OrqagaTugmasi}
      </Page>
    )
  }

  // Qisqa maydonlar (muddat, narx, ...) — faqat to'ldirilganlari ko'rsatiladi.
  const barchaQatorlar: { kalit: TranslationKey; qiymat: string }[] = [
    { kalit: 'service_agency', qiymat: data.idora },
    { kalit: 'service_term', qiymat: data.muddat },
    { kalit: 'service_price', qiymat: data.narx },
    { kalit: 'service_who', qiymat: data.kimlar_uchun },
    { kalit: 'service_contact', qiymat: data.aloqa },
    { kalit: 'service_extra', qiymat: data.qoshimcha },
  ]
  const qatorlar = barchaQatorlar.filter((qator) => qator.qiymat)

  return (
    <Page title={data.nomi}>
      {OrqagaTugmasi}

      <div className={styles.top}>
        <Link to={`/xizmatlar?soha=${encodeURIComponent(data.soha)}`} className={styles.soha}>
          {dataLabel(data.soha, locale)}
        </Link>
        <button
          type="button"
          className={styles.ask}
          onClick={() => {
            open()
            ask(data.nomi, { showQuestion: false })
          }}
        >
          {t('service_ask')}
        </button>
      </div>

      {data.tavsif && <p className={styles.lead}>{data.tavsif}</p>}

      {data.qadamlar.length > 0 && (
        <Bolim sarlavha={t('service_steps')}>
          <ol className={styles.steps}>
            {data.qadamlar.map((qadam, index) => (
              <li key={index}>{qadam}</li>
            ))}
          </ol>
        </Bolim>
      )}

      {data.hujjatlar.length > 0 && (
        <Bolim sarlavha={t('service_documents')}>
          <ul className={styles.bullets}>
            {data.hujjatlar.map((hujjat, index) => (
              <li key={index}>{hujjat}</li>
            ))}
          </ul>
        </Bolim>
      )}

      {qatorlar.length > 0 && (
        <dl className={styles.facts}>
          {qatorlar.map((qator) => (
            <div key={qator.kalit} className={styles.fact}>
              <dt>{t(qator.kalit)}</dt>
              <dd>{qator.qiymat}</dd>
            </div>
          ))}
        </dl>
      )}

      {data.muammolar.length > 0 && (
        <Bolim sarlavha={t('service_problems')}>
          <ul className={styles.bullets}>
            {data.muammolar.map((muammo, index) => (
              <li key={index}>{muammo}</li>
            ))}
          </ul>
        </Bolim>
      )}

      {data.url && (
        <a className={styles.source} href={data.url} target="_blank" rel="noopener noreferrer">
          {t('service_open_source')}
          <Icon name="arrowRight" />
        </a>
      )}
    </Page>
  )
}
