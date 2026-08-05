import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import { App } from '@app/App'
import { applyTheme, readThemeChoice } from '@shared/theme'
import '@shared/styles/global.css'

// Mavzu React'dan oldin qo'llanadi — sahifa boshidanoq to'g'ri rangda chiziladi.
applyTheme(readThemeChoice())

const container = document.getElementById('root')
if (!container) {
  throw new Error('#root elementi topilmadi — index.html buzilgan.')
}

createRoot(container).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
