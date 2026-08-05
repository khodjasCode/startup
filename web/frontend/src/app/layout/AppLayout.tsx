import { useCallback, useEffect, useState } from 'react'
import { Outlet, useLocation } from 'react-router-dom'

import { ChatLauncher, ChatWidget } from '@features/chat'
import { cx } from '@shared/lib/cx'
import { readStorage, writeStorage } from '@shared/lib/storage'
import { useMediaQuery } from '@shared/lib/useMediaQuery'

import { ROUTES } from '../routes'
import styles from './AppLayout.module.css'
import { Footer } from './Footer'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

const SIDEBAR_KEY = 'compass:sidebar'

/** Sahifa karkasi: yon panel + (sarlavha, kontent, pastki qism) + chat qatlami. */
export function AppLayout() {
  const isMobile = useMediaQuery('(max-width: 960px)')
  const { pathname } = useLocation()

  // Katta ekranda oxirgi tanlov eslab qolinadi; kichik ekranda panel doim yopiq
  // holatda ochiladi (u kontent ustidan chiqadi).
  const [isSidebarOpen, setIsSidebarOpen] = useState(() => readStorage(SIDEBAR_KEY) !== 'closed')

  useEffect(() => {
    if (isMobile) setIsSidebarOpen(false)
  }, [isMobile])

  // Sahifa almashganda yuqoriga qaytamiz.
  useEffect(() => {
    window.scrollTo({ top: 0 })
  }, [pathname])

  // Katalogga (yo'nalish sahifasiga) kirilganda yon panel avtomatik yig'iladi —
  // u yerda o'zining yo'nalishlar ustuni bor, ikkitasi yonma-yon keraksiz.
  useEffect(() => {
    if (pathname.startsWith(ROUTES.services)) setIsSidebarOpen(false)
  }, [pathname])

  const toggleSidebar = useCallback(() => {
    setIsSidebarOpen((value) => {
      const next = !value
      if (!isMobile) writeStorage(SIDEBAR_KEY, next ? 'open' : 'closed')
      return next
    })
  }, [isMobile])

  // Havola bosilganda mobil panel yopiladi, katta ekranda ochiq qoladi.
  const closeOnMobile = useCallback(() => {
    if (isMobile) setIsSidebarOpen(false)
  }, [isMobile])

  return (
    <>
      <div className={cx(styles.layout, isSidebarOpen && styles.withSidebar)}>
        <Sidebar isOpen={isSidebarOpen} onClose={closeOnMobile} onToggle={toggleSidebar} />

        <div className={styles.content}>
          <Header onToggleSidebar={toggleSidebar} sidebarOpen={isSidebarOpen} />
          <Outlet />
          <Footer />
        </div>
      </div>

      <ChatWidget />
      <ChatLauncher />
    </>
  )
}
