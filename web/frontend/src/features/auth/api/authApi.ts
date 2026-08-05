import { getJson, postJson } from '@shared/api/httpClient'

export interface User {
  telefon: string
  telefon_korinishi: string
  tugilgan_sana: string
  yaratilgan: string
  /** Foydalanuvchi tanlagan hudud (viloyat) identifikatori. */
  hudud: string
}

interface UserDto {
  foydalanuvchi: User | null
}

export interface SmsResult {
  muddat_soniya: number
  qayta_yuborish_soniya: number
  /** ⚠️ Demo rejim: haqiqiy SMS o'rniga kod shu yerda qaytariladi. */
  mock_kod: string
}

export function fetchMe(signal?: AbortSignal): Promise<User | null> {
  return getJson<UserDto>('/auth/men', signal).then((dto) => dto.foydalanuvchi)
}

export function sendSms(telefon: string, tugilganSana: string): Promise<SmsResult> {
  return postJson<SmsResult>('/auth/sms', { telefon, tugilgan_sana: tugilganSana })
}

export function verifyCode(telefon: string, kod: string, hudud: string): Promise<User | null> {
  return postJson<UserDto>('/auth/tasdiqlash', { telefon, kod, hudud }).then(
    (dto) => dto.foydalanuvchi,
  )
}

export function logout(): Promise<unknown> {
  return postJson('/auth/chiqish', {})
}
