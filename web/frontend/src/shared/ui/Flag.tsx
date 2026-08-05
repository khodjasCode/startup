import type { Locale } from '@shared/i18n'

/**
 * Davlat bayroqlari — SVG sifatida chiziladi, emoji emas: Windows'da bayroq
 * emojilari umuman ko'rinmaydi (o'rniga "UZ", "RU" harflari chiqadi).
 */
const FLAGS: Record<Locale, React.ReactElement> = {
  uz: (
    <>
      <rect width="24" height="5.33" y="0" fill="#0099b5" />
      <rect width="24" height="5.34" y="5.33" fill="#fff" />
      <rect width="24" height="5.33" y="10.67" fill="#1eb53a" />
      <rect width="24" height="0.7" y="5.05" fill="#ce1126" />
      <rect width="24" height="0.7" y="10.25" fill="#ce1126" />
      <circle cx="4.6" cy="2.6" r="1.7" fill="#fff" />
      <circle cx="5.4" cy="2.4" r="1.7" fill="#0099b5" />
    </>
  ),
  ru: (
    <>
      <rect width="24" height="5.33" y="0" fill="#fff" />
      <rect width="24" height="5.34" y="5.33" fill="#0039a6" />
      <rect width="24" height="5.33" y="10.67" fill="#d52b1e" />
    </>
  ),
  en: (
    <>
      <rect width="24" height="16" fill="#012169" />
      <path d="M0 0l24 16M24 0L0 16" stroke="#fff" strokeWidth="3.2" />
      <path d="M0 0l24 16M24 0L0 16" stroke="#c8102e" strokeWidth="1.9" />
      <path d="M12 0v16M0 8h24" stroke="#fff" strokeWidth="5.3" />
      <path d="M12 0v16M0 8h24" stroke="#c8102e" strokeWidth="3.2" />
    </>
  ),
}

export function Flag({ locale, className }: { locale: Locale; className?: string | undefined }) {
  return (
    <svg
      viewBox="0 0 24 16"
      width="20"
      height="14"
      aria-hidden="true"
      focusable="false"
      {...(className ? { className } : {})}
    >
      {FLAGS[locale]}
    </svg>
  )
}
