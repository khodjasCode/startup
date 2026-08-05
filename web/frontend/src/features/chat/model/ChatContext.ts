import { createContext } from 'react'

import type { Chat, ChatMessage } from './types'

export interface AskOptions {
  /**
   * false bo'lsa fuqaro xabari chatda ko'rsatilmaydi (kategoriya kartochkasi
   * bosilganda shunday), lekin serverga xuddi shu tarzda yuboriladi.
   */
  showQuestion?: boolean
}

export interface ChatContextValue {
  /** Barcha suhbatlar (yangisi birinchi). */
  chats: Chat[]
  activeId: string
  /** Ochiq suhbat xabarlari. */
  messages: ChatMessage[]
  /** So'rov yuborilgan va javob kutilyapti. */
  isBusy: boolean
  isOpen: boolean
  /** Yoyilgan holat: panel o'ng chetga, sarlavhadan pastgacha o'rnashadi. */
  isExpanded: boolean
  open: () => void
  close: () => void
  toggle: () => void
  toggleExpanded: () => void
  /** Savol yuborish; panel yopiq bo'lsa avtomatik ochiladi. */
  ask: (question: string, options?: AskOptions) => void
  newChat: () => void
  selectChat: (id: string) => void
  deleteChat: (id: string) => void
}

export const ChatContext = createContext<ChatContextValue | null>(null)
