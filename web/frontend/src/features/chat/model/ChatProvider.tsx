import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import type { ReactNode } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

import { useAuth } from '@features/auth'
import { useI18n } from '@shared/i18n'
import { readStorage, writeStorage } from '@shared/lib/storage'

import { askQuestion, clearConversation } from '../api/chatApi'
import { ChatContext } from './ChatContext'
import type { AskOptions, ChatContextValue } from './ChatContext'
import type { Chat, ChatMessage } from './types'

const CHATS_KEY = 'compass:chats'
const CHATLAR_CHEGARASI = 30 // eng eski suhbatlar shu chegaradan keyin o'chiriladi

function yangiId(): string {
  return crypto.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`
}

function boshSuhbat(): Chat {
  return { id: yangiId(), sarlavha: '', xabarlar: [], yangilangan: Date.now() }
}

/** Suhbatlar brauzerda saqlanadi — sahifa yangilansa ham tarix joyida qoladi. */
function chatlarniOqish(): Chat[] {
  try {
    const xom = readStorage(CHATS_KEY)
    if (!xom) return []
    const royxat = JSON.parse(xom) as Chat[]
    if (!Array.isArray(royxat)) return []
    // Javobini kutib qolgan xabarlar saqlanmasligi kerak edi, ehtiyot uchun tozalaymiz.
    return royxat
      .filter((chat) => chat && typeof chat.id === 'string')
      .map((chat) => ({
        ...chat,
        xabarlar: (chat.xabarlar ?? []).filter((x) => x.status !== 'pending'),
      }))
  } catch {
    return []
  }
}

function chatlarniYozish(chats: Chat[]): void {
  const saqlanadigan = chats
    .filter((chat) => chat.xabarlar.length > 0)
    .slice(0, CHATLAR_CHEGARASI)
    .map((chat) => ({
      ...chat,
      xabarlar: chat.xabarlar.filter((x) => x.status !== 'pending'),
    }))
  writeStorage(CHATS_KEY, JSON.stringify(saqlanadigan))
}

interface ChatProviderProps {
  children: ReactNode
  /**
   * Kirish sahifasining yo'li. Prop orqali beriladi, chunki yo'llar ro'yxati
   * `app` qatlamida (`app/routes.ts`), feature esa undan yuqoriga bog'lanmaydi.
   */
  loginPath: string
}

export function ChatProvider({ children, loginPath }: ChatProviderProps) {
  const { locale } = useI18n()
  const { user, loading: authLoading } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const [chats, setChats] = useState<Chat[]>(() => {
    const saqlangan = chatlarniOqish()
    return saqlangan.length > 0 ? saqlangan : [boshSuhbat()]
  })
  // Boshlang'ich ochiq suhbat — ro'yxatdagi birinchisi. Lazy initializer'da
  // hisoblanadi (render paytida setState chaqirmaslik uchun): shu bitta
  // `chats` massividan olingani uchun ID mos kelishi kafolatlanadi.
  const [activeId, setActiveId] = useState<string>(() => chats[0]?.id ?? '')
  const [isBusy, setIsBusy] = useState(false)
  const [isOpen, setIsOpen] = useState(false)
  const [isExpanded, setIsExpanded] = useState(false)

  useEffect(() => {
    chatlarniYozish(chats)
  }, [chats])

  // Komponent yo'q qilinganda javobni kutayotgan so'rov bekor qilinadi.
  const abortRef = useRef<AbortController | null>(null)
  useEffect(() => () => abortRef.current?.abort(), [])

  const idRef = useRef(0)
  const nextMessageId = useCallback(() => {
    idRef.current += 1
    return `m${idRef.current}`
  }, [])

  /**
   * AI yordamchisi faqat ro'yxatdan o'tganlar uchun: kirmagan foydalanuvchi
   * kirish sahifasiga yo'naltiriladi. Qaysi sahifadan kelgani `state` da
   * saqlanadi — kirgandan so'ng LoginPage uni o'sha yerga qaytaradi va chatni
   * qayta ochadi (`pages/login/LoginPage.tsx` ga qarang).
   */
  const kirishgaYonaltirish = useCallback(() => {
    setIsOpen(false)
    // Kirish sahifasining o'zidan yo'naltirmaymiz: aks holda `qaytish` ga shu
    // sahifaning yo'li tushib qolardi va kirgandan keyin sahifa o'zini o'ziga
    // qaytarib, aylanib qolardi.
    if (location.pathname === loginPath) return
    navigate(loginPath, {
      state: { qaytish: `${location.pathname}${location.search}`, chat: true },
    })
  }, [navigate, loginPath, location.pathname, location.search])

  const close = useCallback(() => setIsOpen(false), [])

  const open = useCallback(() => {
    // `authLoading` — sessiya hali tekshirilmoqda: bu paytda yo'naltirmaymiz,
    // aks holda sahifa yangilangach kirgan foydalanuvchi ham chetga uchardi.
    if (!user && !authLoading) {
      kirishgaYonaltirish()
      return
    }
    setIsOpen(true)
  }, [user, authLoading, kirishgaYonaltirish])

  const toggle = useCallback(() => (isOpen ? close() : open()), [isOpen, close, open])
  const toggleExpanded = useCallback(() => setIsExpanded((value) => !value), [])

  // Sessiya tekshiruvi tugagach yoki muddati o'tib ketgach chat ochiq qolmasin.
  useEffect(() => {
    if (isOpen && !authLoading && !user) kirishgaYonaltirish()
  }, [isOpen, authLoading, user, kirishgaYonaltirish])

  /** Ochiq suhbat xabarlarini yangilaydi va uni ro'yxat boshiga chiqaradi. */
  const suhbatniYangilash = useCallback(
    (id: string, ozgartir: (xabarlar: ChatMessage[]) => ChatMessage[]) => {
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === id
            ? { ...chat, xabarlar: ozgartir(chat.xabarlar), yangilangan: Date.now() }
            : chat,
        ),
      )
    },
    [],
  )

  const newChat = useCallback(() => {
    setChats((prev) => {
      // Bo'sh suhbat allaqachon bo'lsa, yangisini yaratmaymiz.
      const bosh = prev.find((chat) => chat.xabarlar.length === 0)
      if (bosh) {
        setActiveId(bosh.id)
        return prev
      }
      const chat = boshSuhbat()
      setActiveId(chat.id)
      return [chat, ...prev]
    })
  }, [])

  const selectChat = useCallback((id: string) => setActiveId(id), [])

  const deleteChat = useCallback((id: string) => {
    void clearConversation(id).catch(() => {
      /* serverdagi tarixni o'chirib bo'lmadi — brauzerdagisi baribir ketadi */
    })
    setChats((prev) => {
      const qolgan = prev.filter((chat) => chat.id !== id)
      const natija = qolgan.length > 0 ? qolgan : [boshSuhbat()]
      setActiveId((joriy) => (joriy === id ? (natija[0]?.id ?? '') : joriy))
      return natija
    })
  }, [])

  const ask = useCallback(
    (rawQuestion: string, { showQuestion = true }: AskOptions = {}) => {
      const question = rawQuestion.trim()
      if (!question || isBusy) return

      // Xizmat sahifasidan to'g'ridan-to'g'ri ham chaqiriladi, shuning uchun
      // tekshiruv shu yerda ham kerak (sessiya muddati o'tgan bo'lishi mumkin).
      if (!user && !authLoading) {
        kirishgaYonaltirish()
        return
      }

      const chatId = activeId || chats[0]?.id
      if (!chatId) return

      const pendingId = nextMessageId()
      const userId = nextMessageId()

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === chatId
            ? {
                ...chat,
                // Sarlavha — birinchi savol matni.
                sarlavha: chat.sarlavha || question,
                yangilangan: Date.now(),
                xabarlar: [
                  ...chat.xabarlar,
                  ...(showQuestion
                    ? [{ id: userId, role: 'user' as const, text: question, status: 'done' as const }]
                    : []),
                  { id: pendingId, role: 'bot' as const, text: '', status: 'pending' as const },
                ],
              }
            : chat,
        ),
      )
      setIsBusy(true)

      const controller = new AbortController()
      abortRef.current = controller

      askQuestion({ question, sessionId: chatId, locale }, controller.signal)
        .then((answer) => {
          suhbatniYangilash(chatId, (xabarlar) =>
            xabarlar.map((x) => (x.id === pendingId ? { ...x, text: answer, status: 'done' } : x)),
          )
        })
        .catch((error: unknown) => {
          if (controller.signal.aborted) return
          console.error('Savol yuborishda xatolik:', error)
          suhbatniYangilash(chatId, (xabarlar) =>
            xabarlar.map((x) => (x.id === pendingId ? { ...x, status: 'error' } : x)),
          )
        })
        .finally(() => {
          if (!controller.signal.aborted) setIsBusy(false)
          if (abortRef.current === controller) abortRef.current = null
        })
    },
    [
      activeId,
      chats,
      isBusy,
      locale,
      nextMessageId,
      suhbatniYangilash,
      user,
      authLoading,
      kirishgaYonaltirish,
    ],
  )

  const tartiblangan = useMemo(
    () => [...chats].sort((a, b) => b.yangilangan - a.yangilangan),
    [chats],
  )
  const messages = useMemo(
    () => chats.find((chat) => chat.id === activeId)?.xabarlar ?? [],
    [chats, activeId],
  )

  const value = useMemo<ChatContextValue>(
    () => ({
      chats: tartiblangan,
      activeId,
      messages,
      isBusy,
      isOpen,
      isExpanded,
      open,
      close,
      toggle,
      toggleExpanded,
      ask,
      newChat,
      selectChat,
      deleteChat,
    }),
    [
      tartiblangan,
      activeId,
      messages,
      isBusy,
      isOpen,
      isExpanded,
      open,
      close,
      toggle,
      toggleExpanded,
      ask,
      newChat,
      selectChat,
      deleteChat,
    ],
  )

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>
}
