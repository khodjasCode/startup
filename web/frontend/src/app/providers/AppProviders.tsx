import type { ReactNode } from 'react'

import { AuthProvider } from '@features/auth'
import { ChatProvider } from '@features/chat'
import { I18nProvider } from '@shared/i18n'
import { ThemeProvider } from '@shared/theme'

/**
 * Global provayderlar. Tartib muhim: ChatProvider til tanlovini o'qiydi
 * (savol qaysi tilda javob olishini belgilash uchun), shuning uchun u
 * I18nProvider ichida turadi.
 */
export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <I18nProvider>
        <AuthProvider>
          <ChatProvider>{children}</ChatProvider>
        </AuthProvider>
      </I18nProvider>
    </ThemeProvider>
  )
}
