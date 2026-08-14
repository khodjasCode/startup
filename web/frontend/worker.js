// /api/* va /ws/* so'rovlarini serverdagi backendga (origin.yonaltiruvchi.uz)
// proksilaydi. Boshqa hamma yo'l wrangler.toml'dagi [assets] orqali to'g'ridan
// -to'g'ri Cloudflare tomonidan (bu skriptga tegmasdan) beriladi — shuning
// uchun bu yerga faqat run_worker_first ro'yxatidagi so'rovlar keladi.
//
// Bitta domenda ishlagani uchun (cookie ham, /api ham yonaltiruvchi.uz'da)
// frontend kodida hech narsa o'zgartirish shart emas: sessiya cookie'si va
// nisbiy `/api`, `/ws` so'rovlari xuddi backend to'g'ridan-to'g'ri shu
// domenda ishlagandek davom etadi.

export default {
  async fetch(request, env) {
    const url = new URL(request.url)
    const backend = new URL(env.BACKEND_ORIGIN)

    url.protocol = backend.protocol
    url.hostname = backend.hostname
    url.port = backend.port

    const proxied = new Request(url, request)
    proxied.headers.set('Host', backend.hostname)
    proxied.headers.set('X-Forwarded-Proto', 'https')
    proxied.headers.set('X-Forwarded-For', request.headers.get('CF-Connecting-IP') || '')

    return fetch(proxied)
  },
}
