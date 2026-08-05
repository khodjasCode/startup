import type { AnswerBlock } from './types'

/** Bot javobidagi bo'lim sarlavhalari shu emojilardan boshlanadi. */
const HEADING_EMOJI = ['🏢', '📞', '📄', '📝', '🔗']

const STEP_PATTERN = /^\d+[.)]\s/

/**
 * Bot javobi — oddiy matn: emoji bilan boshlanuvchi sarlavhalar, "•" bandlar va
 * "1." qadamlar. Uni o'qishga qulay bo'laklarga ajratamiz; HTML yasalmaydi,
 * shuning uchun injeksiya xavfi yo'q (React matnni o'zi escape qiladi).
 */
export function formatAnswer(text: string): AnswerBlock[] {
  return text
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .map((line) => ({ kind: detectKind(line), text: line }))
}

function detectKind(line: string): AnswerBlock['kind'] {
  if (HEADING_EMOJI.some((emoji) => line.startsWith(emoji))) return 'heading'
  if (line.startsWith('•')) return 'bullet'
  if (STEP_PATTERN.test(line)) return 'step'
  return 'text'
}
