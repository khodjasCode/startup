-- Render'dagi backend uxlab qolmasligi uchun: baza uni o'zi uyg'otib turadi.
--
-- Nega kerak: Render'ning bepul tarifida servis 15 daqiqa murojaatsiz qolsa
-- uxlaydi va keyingi so'rov ~50 soniya kutadi. Har qanday HTTP so'rov uni
-- uyg'otadi — shuning uchun Supabase'ning o'zidagi `pg_cron` shu ishni bajaradi
-- (tashqi xizmatga ro'yxatdan o'tish shart emas).
--
-- Bir marta bajariladi (Supabase → SQL Editor yoki psql orqali).

create extension if not exists pg_cron;
create extension if not exists pg_net;

-- Har 10 daqiqada, UTC 01:00–18:00 oralig'ida = Toshkent vaqti bilan 06:00–23:00.
--
-- Nega sutka bo'yi emas: Render bepul tarifida oyiga 750 "instance soat"
-- beradi, sutka bo'yi ishlash esa ~730 soat — chegaraga deyarli tegib turadi
-- va ikkinchi bepul servis uchun joy qolmaydi. Kunduzgi oyna ~540 soat oladi.
--
-- Sutka bo'yi kerak bo'lsa, jadvalni almashtiring: '*/10 * * * *'
select cron.unschedule(jobid) from cron.job where jobname = 'compass-api-uygotish';

select cron.schedule(
  'compass-api-uygotish',
  '*/10 1-18 * * *',
  $$ select net.http_get(url := 'https://compass-api-x8uy.onrender.com/api/salomatlik') $$
);

-- Tekshirish:
--   select * from cron.job;
--   select status, return_message, start_time from cron.job_run_details
--     order by start_time desc limit 5;
--   select id, status_code, created from net._http_response order by id desc limit 5;
--
-- O'chirish:
--   select cron.unschedule('compass-api-uygotish');
