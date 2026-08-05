import type { ReactElement } from 'react'

/**
 * Yagona ikonka registri — SVG yo'llari faqat shu faylda saqlanadi, komponentlar
 * <Icon name="..." /> orqali ishlatadi.
 */
const PATHS = {
  badge: (
    <path
      fill="currentColor"
      d="M10.586 2.1a2 2 0 0 1 2.7-.116l3.028 2.53a2 2 0 0 0 1.28.463H18a2 2 0 0 1 2 2v1.686l1.9 1.9a2 2 0 0 1 0 2.83l-1.9 1.9V18a2 2 0 0 1-2 2h-2.685l-1.9 1.9a2 2 0 0 1-2.83 0l-1.9-1.9H6a2 2 0 0 1-2-2v-2.685l-1.9-1.9a2 2 0 0 1 0-2.83l1.9-1.9V6a2 2 0 0 1 2-2h1.686l1.9-1.9Z"
    />
  ),
  user: <path fill="currentColor" d="M12 6a3 3 0 1 1 0 6a3 3 0 0 1 0-6Zm0 8c4 0 7 2 7 4v2H5v-2c0-2 3-4 7-4Z" />,
  list: <path fill="currentColor" d="M4 4h16v2H4V4Zm0 7h16v2H4v-2Zm0 7h10v2H4v-2Z" />,
  link: (
    <path
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      d="M10 13a5 5 0 0 0 7 0l2-2a5 5 0 0 0-7-7l-1 1M14 11a5 5 0 0 0-7 0l-2 2a5 5 0 0 0 7 7l1-1"
    />
  ),
  question: (
    <path
      fill="currentColor"
      d="M12 2a10 10 0 1 0 0 20a10 10 0 0 0 0-20Zm.75 15h-1.5v-1.5h1.5V17Zm1.55-6.19c-.6.5-.8.7-.8 1.44v.25h-1.5v-.35c0-1.2.55-1.75 1.15-2.25c.5-.42.85-.72.85-1.35c0-.7-.55-1.2-1.4-1.2c-.75 0-1.35.45-1.5 1.15l-1.45-.3c.3-1.35 1.5-2.35 2.95-2.35c1.65 0 2.9 1.05 2.9 2.6c0 .95-.5 1.5-1.2 2.06Z"
    />
  ),
  phone: (
    <path
      fill="currentColor"
      d="M6.6 10.8c1.2 2.4 3.2 4.4 5.6 5.6l1.9-1.9c.3-.3.7-.4 1-.2c1 .3 2.1.5 3.2.5c.6 0 1 .4 1 1v3.4c0 .6-.4 1-1 1C10.6 20.2 3.8 13.4 3.8 5c0-.6.4-1 1-1H8.2c.6 0 1 .4 1 1c0 1.1.2 2.2.5 3.2c.1.3 0 .7-.2 1L6.6 10.8Z"
    />
  ),
  mail: (
    <path
      fill="currentColor"
      d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4l-8 5l-8-5V6l8 5l8-5v2Z"
    />
  ),
  menu: <path fill="currentColor" d="M3 6h18v2H3V6Zm0 5h18v2H3v-2Zm0 5h18v2H3v-2Z" />,
  /* Yon panelni yig'ish/yoyish belgisi: ramka va uning chap ustuni. */
  panel: (
    <g stroke="currentColor" strokeWidth={1.8} strokeLinejoin="round">
      <rect x="3" y="5" width="18" height="14" rx="2.5" />
      <path d="M9.5 5v14" />
    </g>
  ),
  search: (
    <path
      fill="currentColor"
      d="M21.7 20.3 18 16.6a9 9 0 1 0-1.4 1.4l3.7 3.7a1 1 0 0 0 1.4-1.4ZM11 18a7 7 0 1 1 7-7a7 7 0 0 1-7 7Z"
    />
  ),
  settings: (
    <path
      fill="currentColor"
      d="M12 6a3 3 0 1 1 0 6a3 3 0 0 1 0-6Zm7.4 3a7.4 7.4 0 0 0-.13-1.36l1.98-1.55a.5.5 0 0 0 .12-.64l-1.88-3.26a.5.5 0 0 0-.6-.22l-2.33.94a7.6 7.6 0 0 0-1.18-.68l-.35-2.48a.5.5 0 0 0-.5-.43h-3.75a.5.5 0 0 0-.5.43l-.35 2.48a7.6 7.6 0 0 0-1.18.68l-2.33-.94a.5.5 0 0 0-.6.22L2.63 5.45a.5.5 0 0 0 .12.64L4.73 7.64A7.4 7.4 0 0 0 4.6 9a7.4 7.4 0 0 0 .13 1.36L2.75 11.9a.5.5 0 0 0-.12.64l1.88 3.26a.5.5 0 0 0 .6.22l2.33-.94c.36.28.76.5 1.18.68l.35 2.48a.5.5 0 0 0 .5.43h3.75a.5.5 0 0 0 .5-.43l.35-2.48c.42-.18.82-.4 1.18-.68l2.33.94a.5.5 0 0 0 .6-.22l1.88-3.26a.5.5 0 0 0-.12-.64L19.27 10.36c.08-.44.13-.9.13-1.36Z"
    />
  ),
  chevronDown: (
    <path
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      d="m6 9 6 6 6-6"
    />
  ),
  arrowRight: (
    <path
      fill="currentColor"
      d="M5 13h11.17l-4.88 4.88a1 1 0 1 0 1.41 1.41l6.59-6.58a1 1 0 0 0 0-1.42l-6.58-6.6a1 1 0 1 0-1.42 1.42L16.17 11H5a1 1 0 0 0 0 2Z"
    />
  ),
  minus: <path stroke="currentColor" strokeWidth={2} strokeLinecap="round" d="M5 12h14" />,
  close: (
    <path stroke="currentColor" strokeWidth={2} strokeLinecap="round" d="M6 6l12 12M18 6L6 18" />
  ),
  expand: (
    <path
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M9 4H4v5M15 4h5v5M9 20H4v-5M15 20h5v-5"
    />
  ),
  collapse: (
    <path
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M4 9h5V4M20 9h-5V4M4 15h5v5M20 15h-5v5"
    />
  ),
  plus: <path stroke="currentColor" strokeWidth={2} strokeLinecap="round" d="M12 5v14M5 12h14" />,
  trash: (
    <path
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"
    />
  ),
  sun: (
    <g stroke="currentColor" strokeWidth={2} strokeLinecap="round">
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4" />
    </g>
  ),
  moon: (
    <path
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z"
    />
  ),
  clock: (
    <g stroke="currentColor" strokeWidth={2} strokeLinecap="round">
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3 2" />
    </g>
  ),
  home: <path fill="currentColor" d="M12 3 3 10v11h6v-6h6v6h6V10L12 3Z" />,
  briefcase: (
    <path
      fill="currentColor"
      d="M10 2h4a2 2 0 0 1 2 2v2h4a2 2 0 0 1 2 2v3H2V8a2 2 0 0 1 2-2h4V4a2 2 0 0 1 2-2Zm0 4h4V4h-4v2ZM2 13h20v7a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-7Z"
    />
  ),
  heart: (
    <path
      fill="currentColor"
      d="M12 21s-7-4.35-9.5-8.5C.7 8.9 2.6 5 6.2 5c1.9 0 3.3 1 4 2.4C10.9 6 12.3 5 14.2 5c3.6 0 5.5 3.9 3.7 7.5C19.5 16.65 12 21 12 21Z"
    />
  ),
  land: <path fill="currentColor" d="M3 21V9l9-6l9 6v12h-6v-7H9v7H3Z" />,
  shop: <path fill="currentColor" d="M4 7h16v13H4V7Zm3-4h10a1 1 0 0 1 1 1v2H6V4a1 1 0 0 1 1-1Z" />,
  telegram: (
    <path
      fill="currentColor"
      d="M9.78 18.65l.28-4.23l7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3L3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z"
    />
  ),
  dot: <circle cx="12" cy="12" r="3" fill="currentColor" />,
} satisfies Record<string, ReactElement>

export type IconName = keyof typeof PATHS

interface IconProps {
  name: IconName
  size?: number | undefined
  className?: string | undefined
}

export function Icon({ name, size, className }: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      aria-hidden="true"
      focusable="false"
      {...(size ? { width: size, height: size } : {})}
      {...(className ? { className } : {})}
    >
      {PATHS[name]}
    </svg>
  )
}
