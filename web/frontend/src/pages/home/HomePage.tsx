import { Link } from 'react-router-dom'

import { ROUTES } from '@app/routes'
import { CategoryGrid } from '@features/catalog'
import { useI18n } from '@shared/i18n'
import { Icon } from '@shared/ui/Icon'

import styles from './HomePage.module.css'
import { CtaSection } from './ui/CtaSection'
import { HeroBanner } from './ui/HeroBanner'
import { PromoSection } from './ui/PromoSection'

export function HomePage() {
  const { t } = useI18n()

  return (
    <>
      <HeroBanner />

      <main className={styles.main}>
        <div className={styles.sectionHead}>
          <h2 className={styles.sectionTitle}>{t('nav_categories')}</h2>
          <Link to={ROUTES.categories} className={styles.sectionMore}>
            {t('section_more')}
            <Icon name="arrowRight" />
          </Link>
        </div>

        <CategoryGrid limit={12} />
        <PromoSection />
        <CtaSection />
      </main>
    </>
  )
}
