-- Daily notifications: where subscriptions are stored, and the hourly schedule.
create table if not exists public.push_subs (
  endpoint   text primary key check (char_length(endpoint) < 600),
  p256dh     text not null check (char_length(p256dh) < 200),
  auth       text not null check (char_length(auth) < 100),
  tz         smallint not null default 0 check (tz between -720 and 840),
  hour       smallint not null default 20 check (hour between 0 and 23),
  created_at timestamptz not null default now()
);
alter table public.push_subs enable row level security;
drop policy if exists "Anyone can subscribe" on public.push_subs;
create policy "Anyone can subscribe" on public.push_subs for insert to anon, authenticated with check (true);
revoke all on public.push_subs from anon, authenticated;
grant insert (endpoint, p256dh, auth, tz, hour) on public.push_subs to anon, authenticated;

create extension if not exists pg_cron;
create extension if not exists pg_net;
select cron.schedule('daily-landing-push', '0 * * * *', $$
  select net.http_post(
    url := 'https://mydzixaknqldrcfakirn.supabase.co/functions/v1/daily-push',
    headers := '{"Content-Type":"application/json","x-cron-secret":"YOUR_CRON_SECRET"}'::jsonb,
    body := '{}'::jsonb);
$$);

-- Reminder moved from 8pm to 10am local time (Oct 2026). Run once.
update public.push_subs set hour = 10 where hour = 20;
alter table public.push_subs alter column hour set default 10;
