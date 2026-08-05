/**
 * Web Storage ustidan xavfsiz qobiq: brauzer uni bloklagan (private rejim,
 * cookie taqiqlari) holatda ham ilova yiqilmasligi kerak.
 */
type Area = 'local' | 'session'

function storage(area: Area): Storage | null {
  try {
    return area === 'local' ? window.localStorage : window.sessionStorage
  } catch {
    return null
  }
}

export function readStorage(key: string, area: Area = 'local'): string | null {
  try {
    return storage(area)?.getItem(key) ?? null
  } catch {
    return null
  }
}

export function writeStorage(key: string, value: string, area: Area = 'local'): void {
  try {
    storage(area)?.setItem(key, value)
  } catch {
    /* saqlab bo'lmadi — bu holat ilova ishlashiga to'sqinlik qilmaydi */
  }
}
