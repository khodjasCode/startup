/**
 * CSS klasslarini birlashtiradi: bo'sh/undefined qiymatlar tashlab yuboriladi.
 * CSS-modul kalitlari tipi `string | undefined` bo'lgani uchun kerak.
 */
export function cx(...classes: (string | false | null | undefined)[]): string {
  return classes.filter(Boolean).join(' ')
}
