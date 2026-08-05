import type { ReactNode } from 'react'

import styles from './Page.module.css'

interface PageProps {
  title: string
  subtitle?: string
  actions?: ReactNode
  children: ReactNode
}

/** Ichki sahifalar uchun yagona karkas: sarlavha, izoh va kontent maydoni. */
export function Page({ title, subtitle, actions, children }: PageProps) {
  return (
    <main className={styles.page}>
      <header className={styles.head}>
        <div>
          <h1 className={styles.title}>{title}</h1>
          {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
        </div>
        {actions}
      </header>
      {children}
    </main>
  )
}
