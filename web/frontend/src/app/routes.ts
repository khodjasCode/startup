import type { TranslationKey } from '@shared/i18n'
import type { IconName } from '@shared/ui/Icon'

/** Ilovaning barcha yo'llari bitta joyda — navigatsiya ham shu ro'yxatdan quriladi. */
export const ROUTES = {
  home: '/',
  categories: '/kategoriyalar',
  services: '/xizmatlar',
  service: '/xizmatlar/:id',
  databases: '/bazalar',
  sources: '/manbalar',
  faq: '/savol-javob',
  contact: '/aloqa',
  login: '/kirish',
} as const

export interface NavItem {
  to: string
  labelKey: TranslationKey
  icon: IconName
}

export interface NavSection {
  titleKey: TranslationKey
  items: NavItem[]
}

export const NAV_SECTIONS: NavSection[] = [
  {
    titleKey: 'nav_section_services',
    items: [
      { to: ROUTES.home, labelKey: 'nav_home', icon: 'home' },
      { to: ROUTES.categories, labelKey: 'nav_categories', icon: 'badge' },
      { to: ROUTES.databases, labelKey: 'nav_databases', icon: 'list' },
      { to: ROUTES.sources, labelKey: 'nav_sources', icon: 'link' },
    ],
  },
  {
    titleKey: 'nav_section_help',
    items: [
      { to: ROUTES.faq, labelKey: 'nav_faq', icon: 'question' },
      { to: ROUTES.contact, labelKey: 'nav_contact', icon: 'phone' },
    ],
  },
]
