import { Link } from 'react-router-dom'

import { useI18n } from '@shared/i18n'
import { dataLabel } from '@shared/lib/dataLabels'
import { localizeXizmatQisqa } from '@shared/lib/localizeContent'
import { Icon } from '@shared/ui/Icon'

import type { XizmatQisqa } from '../model/types'
import styles from './ServiceList.module.css'

/**
 * Xizmatlar ro'yxati — qidiruv natijalari va soha sahifalarida ishlatiladi.
 * Nom/tavsif ru/en tanlanganda backend tayyorlagan tarjimaga almashadi
 * (tarjima yo'q bo'lsa asl o'zbekcha matn qoladi).
 */
export function ServiceList({ items }: { items: XizmatQisqa[] }) {
  const { locale } = useI18n()

  return (
    <ul className={styles.list}>
      {items.map((xom) => {
        const xizmat = localizeXizmatQisqa(xom, locale)
        return (
          <li key={xizmat.id}>
            <Link to={`/xizmatlar/${encodeURIComponent(xizmat.id)}`} className={styles.item}>
              <div className={styles.main}>
                <span className={styles.soha}>{dataLabel(xizmat.soha, locale)}</span>
                <h3 className={styles.title}>{xizmat.nomi}</h3>
                {xizmat.tavsif && <p className={styles.text}>{xizmat.tavsif}</p>}
              </div>
              <Icon name="arrowRight" className={styles.arrow} />
            </Link>
          </li>
        )
      })}
    </ul>
  )
}
