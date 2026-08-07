import { getJson, query } from '@shared/api/httpClient'

import type { FaqGuruhi, Manba, Soha, Statistika, Xizmat, XizmatQisqa } from '../model/types'
import { staticKatalog } from './staticKatalog'

/**
 * Backend shuncha vaqt ichida javob bermasa — zaxira manbaga o'tamiz.
 *
 * Nega kerak: bepul hostingda server bir muddat murojaatsiz qolsa uxlaydi va
 * uyg'onishi yarim daqiqagacha cho'zilishi mumkin. Sekin javob xato emas,
 * shuning uchun vaqt chegarasisiz sahifa shuncha vaqt bo'sh turardi — holbuki
 * katalogning to'liq nusxasi shu yerda, statik faylda yotibdi.
 */
const KUTISH_MS = 4000

/**
 * Katalog avval backenddan (/api/...) so'raladi; server javob bermasa yoki
 * sekin bo'lsa (masalan faqat `npm run dev` ishlayotgan bo'lsa yoki server
 * uyg'onayotgan bo'lsa) eksport qilingan /data/katalog.json fayliga
 * o'tiladi — sahifalar baribir to'ladi.
 */
async function zaxiraBilan<T>(asosiy: () => Promise<T>, zaxira: () => Promise<T>): Promise<T> {
  try {
    return await asosiy()
  } catch (xato) {
    if (xato instanceof DOMException && xato.name === 'AbortError') throw xato
    try {
      return await zaxira()
    } catch {
      throw xato // zaxira ham yo'q — asl xatoni qaytaramiz
    }
  }
}

export function fetchSohalar(signal?: AbortSignal): Promise<Soha[]> {
  return zaxiraBilan(
    () => getJson<{ sohalar: Soha[] }>('/sohalar', signal, KUTISH_MS).then((dto) => dto.sohalar),
    () => staticKatalog.sohalar(),
  )
}

export interface XizmatlarParams {
  soha?: string
  q?: string
  limit?: number
  offset?: number
}

export function fetchXizmatlar(
  params: XizmatlarParams,
  signal?: AbortSignal,
): Promise<{ jami: number; xizmatlar: XizmatQisqa[] }> {
  return zaxiraBilan(
    () => getJson(`/xizmatlar${query({ ...params })}`, signal, KUTISH_MS),
    () => staticKatalog.xizmatlar(params),
  )
}

export function fetchXizmat(id: string, signal?: AbortSignal): Promise<Xizmat> {
  return zaxiraBilan(
    () => getJson<Xizmat>(`/xizmatlar/${encodeURIComponent(id)}`, signal, KUTISH_MS),
    () => staticKatalog.xizmat(id),
  )
}

export function fetchManbalar(signal?: AbortSignal): Promise<Manba[]> {
  return zaxiraBilan(
    () => getJson<{ manbalar: Manba[] }>('/manbalar', signal, KUTISH_MS).then((dto) => dto.manbalar),
    () => staticKatalog.manbalar(),
  )
}

export function fetchSavolJavob(
  params: { q?: string },
  signal?: AbortSignal,
): Promise<{ jami: number; guruhlar: FaqGuruhi[] }> {
  return zaxiraBilan(
    () => getJson(`/savol-javob${query({ ...params })}`, signal, KUTISH_MS),
    () => staticKatalog.savolJavob(params),
  )
}

export function fetchStatistika(signal?: AbortSignal): Promise<Statistika> {
  return zaxiraBilan(
    () => getJson<Statistika>('/statistika', signal, KUTISH_MS),
    () => staticKatalog.statistika(),
  )
}
