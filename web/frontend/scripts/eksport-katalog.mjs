// data/*.json → public/data/katalog.json (backend ishlamayotganda ham sayt
// haqiqiy ma'lumot bilan to'lishi uchun). `npm run dev` va `npm run build`
// oldidan avtomatik ishlaydi.
//
// Python topilmasa yoki skript xato bersa — ogohlantirish chiqaradi, lekin
// yig'ishni to'xtatmaydi (avval eksport qilingan fayl bo'lsa, o'shanisi qoladi).

import { spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import { fileURLToPath, URL } from 'node:url'

const ildiz = fileURLToPath(new URL('../../..', import.meta.url))
const natija = fileURLToPath(new URL('../public/data/katalog.json', import.meta.url))

for (const python of ['python', 'python3', 'py']) {
  const jarayon = spawnSync(python, ['-m', 'web.eksport_katalog'], {
    cwd: ildiz,
    stdio: 'inherit',
  })
  if (jarayon.status === 0) process.exit(0)
}

if (existsSync(natija)) {
  console.warn('[eksport-katalog] Python topilmadi — mavjud katalog.json ishlatiladi.')
} else {
  console.warn(
    '[eksport-katalog] Python topilmadi va katalog.json yo‘q — sayt katalogni ' +
      'faqat ishlab turgan backend (/api) orqali ko‘rsatadi.',
  )
}
process.exit(0)
