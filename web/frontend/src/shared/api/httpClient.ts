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

async function sorov<TResponse>(
  yol: string,
  init: RequestInit,
  signal?: AbortSignal,
): Promise<TResponse> {
  let response: Response
  try {
    response = await fetch(`${API_BASE}${yol}`, {
      credentials: 'same-origin', // sessiya cookie'si yuborilishi uchun
      ...init,
      ...(signal ? { signal } : {}),
    })
  } catch (cause) {
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
export function getJson<TResponse>(yol: string, signal?: AbortSignal): Promise<TResponse> {
  return sorov<TResponse>(yol, { method: 'GET' }, signal)
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
