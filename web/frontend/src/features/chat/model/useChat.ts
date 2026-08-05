import { useContext } from 'react'

import { ChatContext } from './ChatContext'
import type { ChatContextValue } from './ChatContext'

export function useChat(): ChatContextValue {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error('useChat faqat <ChatProvider> ichida ishlatiladi.')
  }
  return context
}
