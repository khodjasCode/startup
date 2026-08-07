/** Server kutilmagan javob qaytarganda (HTTP xato yoki noto'g'ri JSON). */
export class ApiError extends Error {
  constructor(
    message: string,
    readonly status?: number,
    /** Backend bergan mashina o'qiydigan sabab (masalan "email_band"). */
    readonly kod?: string,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

const API_BASE = '/api'

/** Vaqt chegarasi tugaganda beriladigan xato kodi (zaxira manbaga o'tish belgisi). */
export const VAQT_TUGADI = 'vaqt_tugadi'

async function sorov<TResponse>(
  yol: string,
  init: RequestInit,
  signal?: AbortSignal,
  kutishMs?: number,
): Promise<TResponse> {
  // O'z boshqaruvimiz: unga ham chaqiruvchining signali, ham vaqt chegarasi
  // ulanadi. Shu tufayli "komponent uzdi" va "server javob bermadi" holatlarini
  // bir-biridan ajratib bo'ladi — birinchisida so'rovni takrorlash kerak emas,
  // ikkinchisida esa zaxira manbaga o'tiladi.
  const boshqaruv = new AbortController()
  let vaqtTugadi = false
  const soat = kutishMs
    ? setTimeout(() => {
        vaqtTugadi = true
        boshqaruv.abort()
      }, kutishMs)
    : undefined
  const uzish = () => boshqaruv.abort()
  signal?.addEventListener('abort', uzish)

  try {
    return await bajarish<TResponse>(yol, init, boshqaruv.signal, () => vaqtTugadi, kutishMs)
  } catch (xato) {
    // Chaqiruvchi bekor qilgan bo'lsa (komponent yo'q qilindi, deps o'zgardi)
    // asl uzilish xatosi qaytariladi — chaqiruvchilar uni `AbortError` bo'yicha
    // taniydi va bekor qilingan so'rovni "xato" deb hisoblamaydi.
    if (signal?.aborted) throw new DOMException("So'rov bekor qilindi", 'AbortError')
    throw xato
  } finally {
    clearTimeout(soat)
    signal?.removeEventListener('abort', uzish)
  }
}

async function bajarish<TResponse>(
  yol: string,
  init: RequestInit,
  signal: AbortSignal,
  vaqtTugadimi: () => boolean,
  kutishMs?: number,
): Promise<TResponse> {
  let response: Response
  try {
    response = await fetch(`${API_BASE}${yol}`, {
      credentials: 'same-origin', // sessiya cookie'si yuborilishi uchun
      ...init,
      signal,
    })
  } catch (cause) {
    if (vaqtTugadimi()) {
      throw new ApiError(`Server ${kutishMs} ms ichida javob bermadi`, undefined, VAQT_TUGADI)
    }
    throw new ApiError(`Serverga ulanib bo'lmadi: ${String(cause)}`)
  }

  if (!response.ok) {
    // FastAPI xatolarni {"detail": "..."} ko'rinishida qaytaradi.
    let kod: string | undefined
    try {
      const tana = (await response.json()) as { detail?: unknown }
      if (typeof tana.detail === 'string') kod = tana.detail
    } catch {
      /* javob JSON emas — kodsiz davom etamiz */
    }
    throw new ApiError(`Server ${response.status} qaytardi`, response.status, kod)
  }

  if (response.status === 204) return undefined as TResponse

  try {
    return (await response.json()) as TResponse
  } catch {
    throw new ApiError("Server javobini JSON sifatida o'qib bo'lmadi")
  }
}

/**
 * Barcha tarmoq murojaatlari shu ikki funksiya orqali o'tadi — feature'lar
 * fetch bilan bevosita ishlamaydi, shuning uchun xatoliklar bir joyda
 * tipizatsiya qilinadi.
 */
/**
 * `kutishMs` berilsa, shu vaqt ichida javob kelmasa so'rov uziladi va
 * `ApiError` (kod `vaqt_tugadi`) ko'tariladi — chaqiruvchi zaxira manbaga
 * o'tishi mumkin. Bermaslik — cheksiz kutish (chat, kirish uchun shunday).
 */
export function getJson<TResponse>(
  yol: string,
  signal?: AbortSignal,
  kutishMs?: number,
): Promise<TResponse> {
  return sorov<TResponse>(yol, { method: 'GET' }, signal, kutishMs)
}

export function postJson<TResponse>(
  yol: string,
  tana: unknown,
  signal?: AbortSignal,
): Promise<TResponse> {
  return sorov<TResponse>(
    yol,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tana),
    },
    signal,
  )
}

/** Query-string yasash (bo'sh qiymatlar tashlab yuboriladi). */
export function query(params: Record<string, string | number | undefined>): string {
  const qidiruv = new URLSearchParams()
  for (const [kalit, qiymat] of Object.entries(params)) {
    if (qiymat === undefined || qiymat === '') continue
    qidiruv.set(kalit, String(qiymat))
  }
  const matn = qidiruv.toString()
  return matn ? `?${matn}` : ''
}
