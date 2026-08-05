export type MessageRole = 'user' | 'bot'

export type MessageStatus = 'pending' | 'done' | 'error'

export interface ChatMessage {
  id: string
  role: MessageRole
  text: string
  status: MessageStatus
}

/** Bitta suhbat. `id` server tarixining kaliti (session_id) sifatida ham ishlatiladi. */
export interface Chat {
  id: string
  sarlavha: string
  xabarlar: ChatMessage[]
  /** Oxirgi o'zgarish vaqti (ms) — ro'yxatni saralash uchun. */
  yangilangan: number
}

/** Bot javobi ko'rsatish uchun bo'laklarga ajratilgan holda. */
export type AnswerBlockKind = 'heading' | 'bullet' | 'step' | 'text'

export interface AnswerBlock {
  kind: AnswerBlockKind
  text: string
}
