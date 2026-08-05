import { useEffect, useState } from 'react'

/** Qiymat o'zgarishini kechiktiradi — har harf uchun so'rov yubormaslik uchun. */
export function useDebounced<T>(value: T, delay = 300): T {
  const [kechikkan, setKechikkan] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => setKechikkan(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])

  return kechikkan
}
