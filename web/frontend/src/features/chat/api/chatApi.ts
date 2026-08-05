import { postJson } from '@shared/api/httpClient'
import type { Locale } from '@shared/i18n'

/** POST /api/savol — so'rov tanasi (backend nomlari o'zgarmaydi). */
interface AskRequestDto {
  savol: string
  session_id: string
  til: Locale
}

/** POST /api/savol — javob tanasi. */
interface AskResponseDto {
  javob: string
}

export interface AskParams {
  question: string
  sessionId: string
  locale: Locale
}

/**
 * Savolni RAG yadrosiga yuboradi va tayyor javob matnini qaytaradi.
 * Backend bilan yagona aloqa nuqtasi — DTO ↔ domen nomlari shu yerda mos keladi.
 */
export async function askQuestion(
  { question, sessionId, locale }: AskParams,
  signal?: AbortSignal,
): Promise<string> {
  const dto = await postJson<AskResponseDto>(
    '/savol',
    { savol: question, session_id: sessionId, til: locale } satisfies AskRequestDto,
    signal,
  )
  return dto.javob
}

/** Serverdagi suhbat tarixini o'chiradi (sozlamalardagi "tozalash" tugmasi). */
export function clearConversation(sessionId: string): Promise<unknown> {
  return postJson('/suhbatni-tozalash', { session_id: sessionId })
}
