import type { uz } from './uz'

/** Tarjima kaliti — o'zbekcha (referens) lug'atdan avtomatik olinadi. */
export type TranslationKey = keyof typeof uz

/** Har bir til shu shaklda bo'lishi shart: bitta kalit ham tushib qolmaydi. */
export type Dictionary = Record<TranslationKey, string>
