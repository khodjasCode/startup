import { useRef } from 'react'

import styles from './DateInput.module.css'

export interface DateValue {
  kun: string
  oy: string
  yil: string
}

export const BOSH_SANA: DateValue = { kun: '', oy: '', yil: '' }

/** DateValue → ISO (yyyy-mm-dd), to'liq kiritilmagan bo'lsa null. */
export function sanaIsoga(qiymat: DateValue): string | null {
  const { kun, oy, yil } = qiymat
  if (kun.length < 1 || oy.length < 1 || yil.length !== 4) return null
  return `${yil}-${oy.padStart(2, '0')}-${kun.padStart(2, '0')}`
}

interface DateInputProps {
  value: DateValue
  onChange: (value: DateValue) => void
  label: string
}

/**
 * Tug'ilgan sana maydoni: kun/oy/yil — brauzer/OS lokaliga bog'liq bo'lmagan
 * qat'iy DD/MM/YYYY tartibida. Native `<input type="date">` bunday nazoratni
 * bermaydi (formati brauzer tiliga qarab o'zgaradi — masalan mm/dd/yyyy).
 */
export function DateInput({ value, onChange, label }: DateInputProps) {
  const oyRef = useRef<HTMLInputElement>(null)
  const yilRef = useRef<HTMLInputElement>(null)

  const kunOzgardi = (xom: string) => {
    const kun = xom.replace(/\D/g, '').slice(0, 2)
    onChange({ ...value, kun })
    if (kun.length === 2) oyRef.current?.focus()
  }

  const oyOzgardi = (xom: string) => {
    const oy = xom.replace(/\D/g, '').slice(0, 2)
    onChange({ ...value, oy })
    if (oy.length === 2) yilRef.current?.focus()
  }

  const yilOzgardi = (xom: string) => {
    onChange({ ...value, yil: xom.replace(/\D/g, '').slice(0, 4) })
  }

  return (
    <label className={styles.field}>
      <span className={styles.label}>{label}</span>
      <div className={styles.box}>
        <input
          className={styles.day}
          value={value.kun}
          onChange={(e) => kunOzgardi(e.target.value)}
          inputMode="numeric"
          placeholder="DD"
          maxLength={2}
          aria-label="DD"
          required
        />
        <span className={styles.sep}>/</span>
        <input
          ref={oyRef}
          className={styles.day}
          value={value.oy}
          onChange={(e) => oyOzgardi(e.target.value)}
          inputMode="numeric"
          placeholder="MM"
          maxLength={2}
          aria-label="MM"
          required
        />
        <span className={styles.sep}>/</span>
        <input
          ref={yilRef}
          className={styles.year}
          value={value.yil}
          onChange={(e) => yilOzgardi(e.target.value)}
          inputMode="numeric"
          placeholder="YYYY"
          maxLength={4}
          aria-label="YYYY"
          required
        />
      </div>
    </label>
  )
}
