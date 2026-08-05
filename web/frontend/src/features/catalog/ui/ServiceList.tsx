import { Link } from 'react-router-dom'

import { useI18n } from '@shared/i18n'
import { dataLabel } from '@shared/lib/dataLabels'
import { Icon } from '@shared/ui/Icon'

import type { XizmatQisqa } from '../model/types'
import styles from './ServiceList.module.css'

/**
 * Xizmatlar ro'yxati — qidiruv natijalari va soha sahifalarida ishlatiladi.
 *
 * Diqqat: xizmat nomi va tavsifi bazada faqat o'zbekcha (329 yozuvni uch
 * tilga tarjima qilish mumkin emas) — tarjima faqat soha yorlig'iga qo'llanadi.
 */
export function ServiceList({ items }: { items: XizmatQisqa[] }) {
  const { locale } = useI18n()

  return (
    <ul className={styles.list}>
      {items.map((xizmat) => (
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
      ))}
    </ul>
  )
}
