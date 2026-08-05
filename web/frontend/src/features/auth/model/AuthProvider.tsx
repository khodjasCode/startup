import { useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'

import * as api from '../api/authApi'
import type { User } from '../api/authApi'
import { AuthContext } from './AuthContext'

/**
 * Sessiya httpOnly cookie'da yuriladi, shuning uchun frontend token bilan
 * umuman ishlamaydi: sahifa ochilganda "men kimman?" so'rovi yuboriladi.
 */
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const controller = new AbortController()
    api
      .fetchMe(controller.signal)
      .then((topilgan) => {
        if (!controller.signal.aborted) setUser(topilgan)
      })
      .catch(() => {
        /* sessiya yo'q yoki server javob bermadi — mehmon rejimida davom etamiz */
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false)
      })
    return () => controller.abort()
  }, [])

  const requestCode = useCallback(
    (telefon: string, tugilganSana: string) => api.sendSms(telefon, tugilganSana),
    [],
  )

  const confirmCode = useCallback(async (telefon: string, kod: string, hudud: string) => {
    setUser(await api.verifyCode(telefon, kod, hudud))
  }, [])

  const logout = useCallback(async () => {
    await api.logout()
    setUser(null)
  }, [])

  const value = useMemo(
    () => ({ user, loading, requestCode, confirmCode, logout }),
    [user, loading, requestCode, confirmCode, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
