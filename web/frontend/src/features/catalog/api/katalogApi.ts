import { getJson, query } from '@shared/api/httpClient'

import type { FaqGuruhi, Manba, Soha, Statistika, Xizmat, XizmatQisqa } from '../model/types'
import { staticKatalog } from './staticKatalog'

/**
 * Katalog avval backenddan (/api/...) so'raladi; server javob bermasa
 * (masalan faqat `npm run dev` ishlayotgan bo'lsa) eksport qilingan
 * /data/katalog.json fayliga o'tiladi — sahifalar baribir to'ladi.
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
    () => getJson<{ sohalar: Soha[] }>('/sohalar', signal).then((dto) => dto.sohalar),
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
    () => getJson(`/xizmatlar${query({ ...params })}`, signal),
    () => staticKatalog.xizmatlar(params),
  )
}

export function fetchXizmat(id: string, signal?: AbortSignal): Promise<Xizmat> {
  return zaxiraBilan(
    () => getJson<Xizmat>(`/xizmatlar/${encodeURIComponent(id)}`, signal),
    () => staticKatalog.xizmat(id),
  )
}

export function fetchManbalar(signal?: AbortSignal): Promise<Manba[]> {
  return zaxiraBilan(
    () => getJson<{ manbalar: Manba[] }>('/manbalar', signal).then((dto) => dto.manbalar),
    () => staticKatalog.manbalar(),
  )
}

export function fetchSavolJavob(
  params: { q?: string },
  signal?: AbortSignal,
): Promise<{ jami: number; guruhlar: FaqGuruhi[] }> {
  return zaxiraBilan(
    () => getJson(`/savol-javob${query({ ...params })}`, signal),
    () => staticKatalog.savolJavob(params),
  )
}

export function fetchStatistika(signal?: AbortSignal): Promise<Statistika> {
  return zaxiraBilan(
    () => getJson<Statistika>('/statistika', signal),
    () => staticKatalog.statistika(),
  )
}
