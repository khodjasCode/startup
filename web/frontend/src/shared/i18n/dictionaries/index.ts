import type { Locale } from '../config'
import { en } from './en'
import { ru } from './ru'
import type { Dictionary } from './types'
import { uz } from './uz'

export const DICTIONARIES: Record<Locale, Dictionary> = { uz, ru, en }

export type { Dictionary, TranslationKey } from './types'
