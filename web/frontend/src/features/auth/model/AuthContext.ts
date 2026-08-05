import { createContext } from 'react'

import type { SmsResult, User } from '../api/authApi'

export interface AuthContextValue {
  user: User | null
  /** Sahifa ochilishida sessiya hali tekshirilmoqda. */
  loading: boolean
  /** Tasdiqlash kodini so'rash (demo rejimda kod javobda qaytadi). */
  requestCode: (telefon: string, tugilganSana: string) => Promise<SmsResult>
  /** Kodni tekshirish va tizimga kirish. */
  confirmCode: (telefon: string, kod: string, hudud: string) => Promise<void>
  logout: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | null>(null)
