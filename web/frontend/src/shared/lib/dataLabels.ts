import type { Locale } from '@shared/i18n'

/**
 * Bazadagi soha/kategoriya nomlari (`data/*.json`) faqat o'zbek tilida —
 * 329 yozuvni uch tilga tarjima qilish mumkin emas, lekin ularning nomlari
 * cheklangan va barqaror to'plam (30 soha, 29 FAQ guruhi), shuning uchun
 * shu nomlar uchun qo'lda tarjima lug'ati yetarli.
 *
 * Kalit — backend qaytaradigan aniq o'zbekcha matn. Yangi soha/guruh paydo
 * bo'lsa (data yangilansa) shu yerga qo'shiladi; topilmasa asl matn qaytadi.
 */
const LABELS: Record<string, Record<Locale, string>> = {
  // ---------- sohalar (xizmatlar) ----------
  Kommunal: { uz: 'Kommunal', ru: 'Коммунальные услуги', en: 'Utilities' },
  "Ma'lumotnomalar": { uz: "Ma'lumotnomalar", ru: 'Справки', en: 'Certificates' },
  'Murojaat (pm.gov.uz)': {
    uz: 'Murojaat (pm.gov.uz)',
    ru: 'Обращения (pm.gov.uz)',
    en: 'Appeals (pm.gov.uz)',
  },
  'Qonunchilik (lex.uz)': {
    uz: 'Qonunchilik (lex.uz)',
    ru: 'Законодательство (lex.uz)',
    en: 'Legislation (lex.uz)',
  },
  Fuqarolik: { uz: 'Fuqarolik', ru: 'Гражданские вопросы', en: 'Civil affairs' },
  'Ijtimoiy himoya': { uz: 'Ijtimoiy himoya', ru: 'Социальная защита', en: 'Social protection' },
  Soliqlar: { uz: 'Soliqlar', ru: 'Налоги', en: 'Taxes' },
  "Sug'urtalash": { uz: "Sug'urtalash", ru: 'Страхование', en: 'Insurance' },
  Pensiya: { uz: 'Pensiya', ru: 'Пенсия', en: 'Pension' },
  Transport: { uz: 'Transport', ru: 'Транспорт', en: 'Transport' },
  'Madaniyat, turizm va sport': {
    uz: 'Madaniyat, turizm va sport',
    ru: 'Культура, туризм и спорт',
    en: 'Culture, tourism & sport',
  },
  'Oila va bolalar': { uz: 'Oila va bolalar', ru: 'Семья и дети', en: 'Family & children' },
  "Sog'liqni saqlash": { uz: "Sog'liqni saqlash", ru: 'Здравоохранение', en: 'Healthcare' },
  Subsidiya: { uz: 'Subsidiya', ru: 'Субсидии', en: 'Subsidies' },
  'Axborot va aloqa': { uz: 'Axborot va aloqa', ru: 'Связь и информация', en: 'Communications' },
  'Bandlik va mehnat': { uz: 'Bandlik va mehnat', ru: 'Занятость и труд', en: 'Employment & labor' },
  Bojxona: { uz: 'Bojxona', ru: 'Таможня', en: 'Customs' },
  Ekologiya: { uz: 'Ekologiya', ru: 'Экология', en: 'Ecology' },
  "Qishloq xo'jaligi": { uz: "Qishloq xo'jaligi", ru: 'Сельское хозяйство', en: 'Agriculture' },
  "Ta'lim": { uz: "Ta'lim", ru: 'Образование', en: 'Education' },
  Adliya: { uz: 'Adliya', ru: 'Юстиция', en: 'Justice' },
  'Davlat aktivlari': { uz: 'Davlat aktivlari', ru: 'Государственные активы', en: 'State assets' },
  'Iqtisodiyot va biznes': {
    uz: 'Iqtisodiyot va biznes',
    ru: 'Экономика и бизнес',
    en: 'Economy & business',
  },
  "Ko'chmas mulk": { uz: "Ko'chmas mulk", ru: 'Недвижимость', en: 'Real estate' },
  Yoshlar: { uz: 'Yoshlar', ru: 'Молодёжь', en: 'Youth' },
  Geologiya: { uz: 'Geologiya', ru: 'Геология', en: 'Geology' },
  "Iste'molchi": { uz: "Iste'molchi", ru: 'Права потребителей', en: 'Consumer rights' },
  Mehnat: { uz: 'Mehnat', ru: 'Труд', en: 'Labor' },
  Tadbirkorlik: { uz: 'Tadbirkorlik', ru: 'Предпринимательство', en: 'Entrepreneurship' },
  'Yer-mulk': { uz: 'Yer-mulk', ru: 'Земля и имущество', en: 'Land & property' },

  // ---------- savol-javob guruhlari ----------
  'Huquqiy javob (lex.uz)': {
    uz: 'Huquqiy javob (lex.uz)',
    ru: 'Правовые ответы (lex.uz)',
    en: 'Legal answers (lex.uz)',
  },
  'Ajrim va aliment masalalari': {
    uz: 'Ajrim va aliment masalalari',
    ru: 'Развод и алименты',
    en: 'Divorce & alimony',
  },
  "Avtohuquq — yo'ldagi huquq": {
    uz: "Avtohuquq — yo'ldagi huquq",
    ru: 'Автоправо — на дороге',
    en: 'Road & driving law',
  },
  'Fuqarolik masalalari': { uz: 'Fuqarolik masalalari', ru: 'Гражданские дела', en: 'Civil matters' },
  'Kommunal xizmatlar': { uz: 'Kommunal xizmatlar', ru: 'Коммунальные услуги', en: 'Utility services' },
  Migratsiya: { uz: 'Migratsiya', ru: 'Миграция', en: 'Migration' },
  Notariat: { uz: 'Notariat', ru: 'Нотариат', en: 'Notary' },
  'Oilaviy munosabatlar': { uz: 'Oilaviy munosabatlar', ru: 'Семейные отношения', en: 'Family relations' },
  'Pensiya va nafaqalar': { uz: 'Pensiya va nafaqalar', ru: 'Пенсии и пособия', en: 'Pensions & benefits' },
  'Uy-joy ijara masalalari': {
    uz: 'Uy-joy ijara masalalari',
    ru: 'Аренда жилья',
    en: 'Housing rental',
  },
  'Bepul huquqiy yordam': {
    uz: 'Bepul huquqiy yordam',
    ru: 'Бесплатная юридическая помощь',
    en: 'Free legal aid',
  },
  'Haydovchilik huquqini olish': {
    uz: 'Haydovchilik huquqini olish',
    ru: 'Получение водительских прав',
    en: "Getting a driver's license",
  },
  "Nogironligi bo'lgan shaxslarga imtiyozlar": {
    uz: "Nogironligi bo'lgan shaxslarga imtiyozlar",
    ru: 'Льготы для людей с инвалидностью',
    en: 'Benefits for people with disabilities',
  },
  'Umumiy harbiy majburiyat': {
    uz: 'Umumiy harbiy majburiyat',
    ru: 'Всеобщая воинская обязанность',
    en: 'Military service duty',
  },
  "Uy-joy, yer va kommunal masalalari": {
    uz: "Uy-joy, yer va kommunal masalalari",
    ru: 'Жильё, земля и коммунальные вопросы',
    en: 'Housing, land & utilities',
  },
  'Abituriyentlar uchun': { uz: 'Abituriyentlar uchun', ru: 'Для абитуриентов', en: 'For applicants' },
  'Bank sohasi': { uz: 'Bank sohasi', ru: 'Банковская сфера', en: 'Banking' },
  'Ishdagi muammolar': { uz: 'Ishdagi muammolar', ru: 'Проблемы на работе', en: 'Workplace issues' },
  'Ishonch telefonlari': { uz: 'Ishonch telefonlari', ru: 'Телефоны доверия', en: 'Helplines' },
  "Iste'molchi huquqi": { uz: "Iste'molchi huquqi", ru: 'Права потребителей', en: 'Consumer rights' },
  'Mehnat munosabatlari': { uz: 'Mehnat munosabatlari', ru: 'Трудовые отношения', en: 'Labor relations' },
  // "Ta'lim" sohalar bo'limida allaqachon aniqlangan — kalitlar bir xil bo'lgani
  // uchun bu yerda takrorlanmaydi (JS obyektida bir xil kalit ikki marta bo'lmaydi).
  Mahalla: { uz: 'Mahalla', ru: 'Махалля', en: 'Mahalla (neighborhood)' },
  'Majburiy ijro': { uz: 'Majburiy ijro', ru: 'Принудительное исполнение', en: 'Enforcement proceedings' },
  'Boshqa savollar': { uz: 'Boshqa savollar', ru: 'Другие вопросы', en: 'Other questions' },
}

/** Bazadan kelgan (o'zbekcha) nomni joriy tilga o'giradi; topilmasa asl matn qaytadi. */
export function dataLabel(uzbekcha: string, locale: Locale): string {
  return LABELS[uzbekcha]?.[locale] ?? uzbekcha
}
