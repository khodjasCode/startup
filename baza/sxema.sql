-- Compass — PostgreSQL sxemasi (Supabase).
-- Qayta-qayta bajarilishi mumkin: barcha buyruqlar `if not exists` bilan.
-- Yaratish/yangilash: python3 -m baza.kochirish

-- RAG qidiruvi uchun vektor turi (Supabase'da mavjud, yoqib qo'yish kifoya).
create extension if not exists vector;

-- ── Katalog: xizmatlar, savol-javoblar, manbalar ──────────────────────────────

create table if not exists xizmatlar (
    -- "my-gov.123" ko'rinishidagi to'liq id (manba kaliti + manbadagi id).
    id            text primary key,
    manba         text        not null,
    soha          text        not null default 'Boshqa',
    nomi          text        not null,
    tavsif        text        not null default '',
    url           text        not null default '',
    -- Yozuv "savol-javob" ko'rinishidami (xizmat emas, huquqiy savolga javob).
    faq           boolean     not null default false,
    kategoriya    text        not null default '',
    muammolar     jsonb       not null default '[]'::jsonb,
    qadamlar      jsonb       not null default '[]'::jsonb,
    hujjatlar     jsonb       not null default '[]'::jsonb,
    muddat        text        not null default '',
    narx          text        not null default '',
    aloqa         text        not null default '',
    kimlar_uchun  text        not null default '',
    idora         text        not null default '',
    qoshimcha     text        not null default '',
    -- Manba fayllaridagi asl tartib — saytda ro'yxat shu ketma-ketlikda ko'rinadi.
    tartib        integer     not null default 0,
    yangilangan   timestamptz not null default now()
);

create index if not exists xizmatlar_soha_idx on xizmatlar (soha);
create index if not exists xizmatlar_faq_idx on xizmatlar (faq);
create index if not exists xizmatlar_manba_idx on xizmatlar (manba);

create table if not exists manbalar (
    kalit          text primary key,
    nomi           text        not null,
    url            text        not null default '',
    tavsif         text        not null default '',
    aloqa          text        not null default '',
    kirish_tartibi jsonb       not null default '[]'::jsonb,
    yigilgan_sana  text        not null default '',
    xizmatlar_soni integer     not null default 0,
    tartib         integer     not null default 0,
    yangilangan    timestamptz not null default now()
);

-- Sxema oldingi versiyada yaratilgan bo'lsa `tartib` ustuni yo'q — qo'shib qo'yamiz.
alter table xizmatlar add column if not exists tartib integer not null default 0;
alter table manbalar add column if not exists tartib integer not null default 0;

-- Ru/en tarjimalari. `tur` — nimaning tarjimasi ('xizmat' yoki 'manba'),
-- `kalit` — xizmat id'si yoki manba kaliti, `qiymat` — tarjima qilingan maydonlar.
create table if not exists tarjimalar (
    tur    text  not null,
    kalit  text  not null,
    til    text  not null,
    qiymat jsonb not null,
    primary key (tur, kalit, til)
);

-- ── Foydalanuvchilar: telefon → SMS kod → sessiya ─────────────────────────────

create table if not exists foydalanuvchilar (
    telefon       text primary key,          -- 998XXXXXXXXX
    tugilgan_sana date        not null,
    hudud         text        not null default '',
    yaratilgan    timestamptz not null default now()
);

create table if not exists sessiyalar (
    token      text primary key,
    telefon    text        not null references foydalanuvchilar (telefon) on delete cascade,
    muddat     timestamptz not null,
    yaratilgan timestamptz not null default now()
);

create index if not exists sessiyalar_muddat_idx on sessiyalar (muddat);

-- Bir telefon uchun bir vaqtda bitta amaldagi kod (shuning uchun telefon — kalit).
create table if not exists kirish_kodlari (
    telefon       text primary key,
    kod           text        not null,
    tugilgan_sana date        not null,
    yuborilgan    timestamptz not null default now(),
    muddat        timestamptz not null,
    urinishlar    integer     not null default 0
);

-- ── Suhbatlar: web chat va Telegram bot tarixi ────────────────────────────────

create table if not exists suhbat_xabarlari (
    id         bigserial primary key,
    -- 'web' uchun brauzerdagi suhbat id'si, 'telegram' uchun chat id.
    sessiya_id text        not null,
    kanal      text        not null default 'web',
    rol        text        not null,          -- 'fuqaro' | 'bot'
    matn       text        not null,
    til        text        not null default 'uz',
    vaqt       timestamptz not null default now()
);

create index if not exists suhbat_xabarlari_sessiya_idx
    on suhbat_xabarlari (kanal, sessiya_id, id);

-- ── RAG: vektor qidiruv bazasi ────────────────────────────────────────────────
-- Ilgari ChromaDB (diskdagi fayl) edi. Endi shu jadval: bulutda ishlayotgan
-- serverda diskni saqlab qolish shart emas va bot bilan web bir xil bazadan
-- qidiradi. `hujjat` — manba yozuvining JSON matni, u LLM'ga kontekst sifatida
-- beriladi (Chroma'dagi `documents` bilan bir xil).
--
-- gemini-embedding-001 → 3072 o'lchov, vektorlar normallashtirilgan (|v| = 1),
-- shuning uchun kosinus masofasi (`<=>`) bilan L2 bir xil tartib beradi.
-- Yozuvlar ~330 ta: indekssiz to'liq ko'rib chiqish ham millisekundlarda
-- bajariladi (hnsw/ivfflat esa 2000 o'lchovgacha cheklangan).
create table if not exists vektorlar (
    id          text primary key,
    manba       text        not null default '',
    hujjat      text        not null,
    embedding   vector(3072) not null,
    yangilangan timestamptz not null default now()
);

-- Telegram foydalanuvchisi tanlagan javob tili (bot qayta ishga tushsa saqlanadi).
create table if not exists telegram_foydalanuvchilari (
    chat_id     bigint primary key,
    til         text        not null default 'uz',
    yangilangan timestamptz not null default now()
);
