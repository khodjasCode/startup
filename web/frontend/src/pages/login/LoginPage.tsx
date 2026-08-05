import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'

import { useAuth } from '@features/auth'
import { ROUTES } from '@app/routes'
import { ApiError } from '@shared/api/httpClient'
import { useI18n } from '@shared/i18n'
import type { TranslationKey } from '@shared/i18n'
import { DEFAULT_REGION, REGIONS } from '@shared/lib/regions'
import { BOSH_SANA, DateInput, sanaIsoga } from '@shared/ui/DateInput'
import type { DateValue } from '@shared/ui/DateInput'
import { Icon } from '@shared/ui/Icon'

import styles from './LoginPage.module.css'

/** Backend xato kodi → tarjima kaliti. */
const XATOLAR: Record<string, TranslationKey> = {
  telefon_notogri: 'err_telefon_notogri',
  sana_notogri: 'err_sana_notogri',
  yosh_kichik: 'err_yosh_kichik',
  sana_mos_emas: 'err_sana_mos_emas',
  tez_tez: 'err_tez_tez',
  kod_notogri: 'err_kod_notogri',
  kod_eskirgan: 'err_kod_eskirgan',
  urinishlar_tugadi: 'err_urinishlar_tugadi',
}

/** 901234567 → "90 123 45 67" (kiritish paytida o'qish uchun). */
function raqamniFormatlash(xom: string): string {
  const raqamlar = xom.replace(/\D/g, '').slice(0, 9)
  const qismlar = [raqamlar.slice(0, 2), raqamlar.slice(2, 5), raqamlar.slice(5, 7), raqamlar.slice(7, 9)]
  return qismlar.filter(Boolean).join(' ')
}

export function LoginPage() {
  const { t, locale } = useI18n()
  const { user, loading, requestCode, confirmCode } = useAuth()
  const navigate = useNavigate()

  const [qadam, setQadam] = useState<'telefon' | 'kod'>('telefon')
  const [telefon, setTelefon] = useState('')
  const [sana, setSana] = useState<DateValue>(BOSH_SANA)
  const [hudud, setHudud] = useState(DEFAULT_REGION)
  const [kod, setKod] = useState('')
  const [mockKod, setMockKod] = useState('')
  const [kutish, setKutish] = useState(0)
  const [xato, setXato] = useState<TranslationKey | null>(null)
  const [band, setBand] = useState(false)

  // Qayta yuborish taymeri.
  useEffect(() => {
    if (kutish <= 0) return
    const timer = setTimeout(() => setKutish((v) => v - 1), 1000)
    return () => clearTimeout(timer)
  }, [kutish])

  if (!loading && user) return <Navigate to={ROUTES.home} replace />

  const xatoniKorsatish = (error: unknown) => {
    const kodi = error instanceof ApiError ? error.kod : undefined
    setXato((kodi && XATOLAR[kodi]) || 'state_error')
  }

  const sanaIso = sanaIsoga(sana)

  const kodSorash = async (event?: FormEvent) => {
    event?.preventDefault()
    if (band || !sanaIso) return
    setXato(null)
    setBand(true)
    try {
      const natija = await requestCode(`998${telefon.replace(/\D/g, '')}`, sanaIso)
      setMockKod(natija.mock_kod)
      setKutish(natija.qayta_yuborish_soniya)
      setQadam('kod')
      setKod('')
    } catch (error) {
      xatoniKorsatish(error)
    } finally {
      setBand(false)
    }
  }

  const kodniTasdiqlash = async (event: FormEvent) => {
    event.preventDefault()
    if (band) return
    setXato(null)
    setBand(true)
    try {
      await confirmCode(`998${telefon.replace(/\D/g, '')}`, kod, hudud)
      navigate(ROUTES.home, { replace: true })
    } catch (error) {
      xatoniKorsatish(error)
    } finally {
      setBand(false)
    }
  }

  return (
    <main className={styles.page}>
      <div className={styles.inner}>
        <header className={styles.head}>
          <h1 className={styles.title}>{t('login_welcome')}</h1>
          <p className={styles.subtitle}>{t('login_welcome_sub')}</p>
        </header>

        <div className={styles.columns}>
          <section className={styles.card}>
            <h2 className={styles.cardTitle}>{t('login_card_title')}</h2>
            <p className={styles.cardHint}>
              {qadam === 'telefon' ? t('login_card_hint') : t('login_mock_notice')}
            </p>

            {qadam === 'telefon' ? (
              <form className={styles.form} onSubmit={kodSorash}>
                <label className={styles.field}>
                  <span className={styles.label}>{t('login_phone')}</span>
                  <div className={styles.phoneBox}>
                    <span className={styles.prefix}>+998</span>
                    <input
                      className={styles.phoneInput}
                      value={raqamniFormatlash(telefon)}
                      onChange={(e) => setTelefon(e.target.value.replace(/\D/g, '').slice(0, 9))}
                      inputMode="numeric"
                      autoComplete="tel-national"
                      placeholder="90 123 45 67"
                      required
                    />
                  </div>
                </label>

                <DateInput value={sana} onChange={setSana} label={t('login_birthdate')} />

                <label className={styles.field}>
                  <span className={styles.label}>{t('login_region')}</span>
                  <select
                    className={styles.input}
                    value={hudud}
                    onChange={(e) => setHudud(e.target.value)}
                  >
                    {REGIONS.map((region) => (
                      <option key={region.id} value={region.id}>
                        {region.nomi[locale]}
                      </option>
                    ))}
                  </select>
                  <span className={styles.hint}>{t('login_region_hint')}</span>
                </label>

                {xato && (
                  <p className={styles.error} role="alert">
                    {t(xato)}
                  </p>
                )}

                <button
                  type="submit"
                  className={styles.submit}
                  disabled={band || telefon.length < 9 || !sanaIso}
                >
                  {t('login_continue')}
                  <Icon name="arrowRight" />
                </button>
              </form>
            ) : (
              <form className={styles.form} onSubmit={kodniTasdiqlash}>
                <div className={styles.sentTo}>
                  <span>{t('login_code_sent')}</span>
                  <strong>+998 {raqamniFormatlash(telefon)}</strong>
                </div>

                {/* Demo rejim: SMS o'rniga kod shu yerda ko'rsatiladi. */}
                <div className={styles.mock}>
                  <span>{t('login_code_label')}</span>
                  <b className={styles.mockCode}>{mockKod}</b>
                </div>

                <label className={styles.field}>
                  <span className={styles.label}>{t('login_code_title')}</span>
                  <input
                    className={styles.codeInput}
                    value={kod}
                    onChange={(e) => setKod(e.target.value.replace(/\D/g, '').slice(0, 6))}
                    inputMode="numeric"
                    autoComplete="one-time-code"
                    placeholder="______"
                    maxLength={6}
                    required
                    autoFocus
                  />
                </label>

                {xato && (
                  <p className={styles.error} role="alert">
                    {t(xato)}
                  </p>
                )}

                <button type="submit" className={styles.submit} disabled={band || kod.length < 6}>
                  {t('login_code_confirm')}
                </button>

                <div className={styles.actions}>
                  <button
                    type="button"
                    className={styles.linkBtn}
                    onClick={() => {
                      setQadam('telefon')
                      setXato(null)
                    }}
                  >
                    {t('login_change_phone')}
                  </button>
                  <button
                    type="button"
                    className={styles.linkBtn}
                    onClick={() => void kodSorash()}
                    disabled={kutish > 0 || band}
                  >
                    {kutish > 0 ? `${t('login_resend_in')} ${kutish}s` : t('login_resend')}
                  </button>
                </div>
              </form>
            )}
          </section>

          <aside className={styles.side}>
            <h2 className={styles.sideTitle}>{t('nav_faq')}</h2>
            {([
              ['login_help_q1', 'login_help_a1'],
              ['login_help_q2', 'login_help_a2'],
              ['login_help_q3', 'login_help_a3'],
            ] as const).map(([savol, javob]) => (
              <details key={savol} className={styles.sideItem}>
                <summary className={styles.sideQuestion}>{t(savol)}</summary>
                <p className={styles.sideAnswer}>{t(javob)}</p>
              </details>
            ))}

            <div className={styles.help}>
              <Icon name="phone" />
              <div>
                <b>{t('login_help_title')}</b>
                <p>{t('login_help_text')}</p>
                <Link to={ROUTES.contact} className={styles.helpLink}>
                  {t('nav_contact')}
                </Link>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </main>
  )
}
