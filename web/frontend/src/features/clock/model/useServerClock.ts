import { useEffect, useRef, useState } from 'react'

interface VaqtXabari {
  iso: string
  mintaqa: string
  ms: number
}

export interface ClockState {
  /** Toshkent vaqti (soat, daqiqa, soniya). */
  soat: number
  daqiqa: number
  soniya: number
  /** Vaqt serverdan olinyaptimi yoki brauzer o'zi hisoblayaptimi. */
  ulangan: boolean
}

const MINTAQA = 'Asia/Tashkent'

/** Brauzer soatidan Toshkent vaqtini hisoblash (zaxira variant). */
function mahalliyToshkentVaqti(): { soat: number; daqiqa: number; soniya: number } {
  const qismlar = new Intl.DateTimeFormat('en-GB', {
    timeZone: MINTAQA,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).formatToParts(new Date())

  const olish = (turi: string) => Number(qismlar.find((q) => q.type === turi)?.value ?? 0)
  return { soat: olish('hour'), daqiqa: olish('minute'), soniya: olish('second') }
}

/**
 * Toshkent vaqti WebSocket (/ws/vaqt) orqali serverdan keladi — foydalanuvchi
 * kompyuteridagi soat noto'g'ri qo'yilgan bo'lsa ham vaqt to'g'ri ko'rinadi.
 * Ulanish bo'lmasa (backend o'chiq) brauzer o'zi hisoblaydi va har soniyada
 * yangilaydi; ulanish qayta tiklanishga urinib turadi.
 */
export function useServerClock(): ClockState {
  const [holat, setHolat] = useState<ClockState>(() => ({
    ...mahalliyToshkentVaqti(),
    ulangan: false,
  }))

  // Serverdan kelgan vaqt va u kelgan lahza — oradagi soniyalarni o'zimiz sanaymiz.
  const asosRef = useRef<{ vaqt: number; olingan: number } | null>(null)

  useEffect(() => {
    let socket: WebSocket | null = null
    let qaytaUlanish: ReturnType<typeof setTimeout> | null = null
    let yopilgan = false

    const ulanish = () => {
      if (yopilgan) return
      const protokol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      try {
        socket = new WebSocket(`${protokol}//${window.location.host}/ws/vaqt`)
      } catch {
        return
      }

      socket.onmessage = (event) => {
        try {
          const xabar = JSON.parse(String(event.data)) as VaqtXabari
          const vaqt = new Date(xabar.iso).getTime() + xabar.ms
          asosRef.current = { vaqt, olingan: performance.now() }
        } catch {
          /* noto'g'ri xabar — e'tiborsiz qoldiramiz */
        }
      }

      socket.onclose = () => {
        asosRef.current = null
        if (!yopilgan) qaytaUlanish = setTimeout(ulanish, 5000)
      }
      socket.onerror = () => socket?.close()
    }

    ulanish()

    // Sekundomer: har 200 ms da tekshiramiz, shuning uchun soniya deyarli aniq
    // lahzada almashadi (1000 ms li interval sekin-asta "suzib" ketardi).
    const tiker = setInterval(() => {
      const asos = asosRef.current
      if (asos) {
        const hozir = new Date(asos.vaqt + (performance.now() - asos.olingan))
        const qismlar = new Intl.DateTimeFormat('en-GB', {
          timeZone: MINTAQA,
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false,
        }).formatToParts(hozir)
        const olish = (turi: string) => Number(qismlar.find((q) => q.type === turi)?.value ?? 0)
        setHolat({
          soat: olish('hour'),
          daqiqa: olish('minute'),
          soniya: olish('second'),
          ulangan: true,
        })
      } else {
        setHolat({ ...mahalliyToshkentVaqti(), ulangan: false })
      }
    }, 200)

    return () => {
      yopilgan = true
      clearInterval(tiker)
      if (qaytaUlanish) clearTimeout(qaytaUlanish)
      socket?.close()
    }
  }, [])

  return holat
}
