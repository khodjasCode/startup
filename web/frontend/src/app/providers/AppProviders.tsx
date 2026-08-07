import type { ReactNode } from 'react'

import { AuthProvider } from '@features/auth'
import { ChatProvider } from '@features/chat'
import { I18nProvider } from '@shared/i18n'
import { ThemeProvider } from '@shared/theme'

import { ROUTES } from '../routes'

/**
 * Global provayderlar. Tartib muhim:
 *  · ChatProvider til tanlovini o'qiydi (savol qaysi tilda javob olishi uchun)
 *    — shuning uchun I18nProvider ichida;
 *  · chat kirmagan foydalanuvchini kirish sahifasiga yuboradi, ya'ni sessiya
 *    holatini biladi — shuning uchun AuthProvider ichida.
 */
export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <I18nProvider>
        <AuthProvider>
          <ChatProvider loginPath={ROUTES.login}>{children}</ChatProvider>
        </AuthProvider>
      </I18nProvider>
    </ThemeProvider>
  )
}
