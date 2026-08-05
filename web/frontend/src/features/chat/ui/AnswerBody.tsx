import { useMemo } from 'react'

import { formatAnswer } from '../model/formatAnswer'
import styles from './AnswerBody.module.css'

/** Bot javobini bo'lim / band / qadam ko'rinishida chiqaradi. */
export function AnswerBody({ text }: { text: string }) {
  const blocks = useMemo(() => formatAnswer(text), [text])

  return (
    <>
      {blocks.map((block, index) => (
        <div key={`${block.kind}-${index}`} className={styles[block.kind]}>
          {block.text}
        </div>
      ))}
    </>
  )
}
