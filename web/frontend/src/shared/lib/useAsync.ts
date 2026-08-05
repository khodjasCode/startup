import { useEffect, useState } from 'react'

export interface AsyncState<T> {
  data: T | null
  loading: boolean
  error: boolean
}

/**
 * Ma'lumot yuklashning uchta holati (yuklanmoqda / xato / tayyor) bir joyda.
 * `deps` o'zgarganda so'rov qayta yuboriladi, eskisi bekor qilinadi.
 */
export function useAsync<T>(
  fetcher: (signal: AbortSignal) => Promise<T>,
  deps: readonly unknown[],
): AsyncState<T> {
  const [state, setState] = useState<AsyncState<T>>({ data: null, loading: true, error: false })

  useEffect(() => {
    const controller = new AbortController()
    setState((prev) => ({ data: prev.data, loading: true, error: false }))

    fetcher(controller.signal)
      .then((data) => {
        if (!controller.signal.aborted) setState({ data, loading: false, error: false })
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return
        console.error('Maʼlumotni yuklab boʻlmadi:', error)
        setState({ data: null, loading: false, error: true })
      })

    return () => controller.abort()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  return state
}
