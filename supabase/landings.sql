-- Now You Have Landed: weekly leaderboard table
-- Run once in Supabase: SQL Editor, New query, paste, Run.

create table if not exists public.landings (
  id         bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  name       text not null default 'Anonymous lander' check (char_length(name) between 1 and 20),
  route      text not null check (route in ('us', 'uk', 'ca')),
  town       text not null check (char_length(town) between 1 and 40),
  verdict    text not null check (char_length(verdict) between 1 and 40),
  score      smallint not null check (score between 0 and 100),
  refused    smallint not null default 0 check (refused between 0 and 30),
  sent       integer  not null default 0 check (sent between 0 and 20000),
  fooled     smallint not null default 0 check (fooled between 0 and 10),
  daily      boolean  not null default false
);

create index if not exists landings_created_at_idx on public.landings (created_at desc);

-- Row level security: anyone can read the board and add a result. Nobody can edit or delete.
alter table public.landings enable row level security;

drop policy if exists "Anyone can read the board" on public.landings;
create policy "Anyone can read the board" on public.landings
  for select to anon, authenticated using (true);

drop policy if exists "Anyone can post a result" on public.landings;
create policy "Anyone can post a result" on public.landings
  for insert to anon, authenticated with check (true);

-- Browsers may only read, and may only fill these columns when adding a row.
revoke all on public.landings from anon, authenticated;
grant select on public.landings to anon, authenticated;
grant insert (name, route, town, verdict, score, refused, sent, fooled, daily) on public.landings to anon, authenticated;

-- Spam protection (added later). Run this part on its own if the table already exists.
-- Limits: 20 posts a minute across everyone, 20 posts an hour per name, and no rude names.
create or replace function public.landings_guard() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.name ~* '(f+u+c+k|sh[i1]t|b[i1]tch|cunt|n[i1]gg|whore|slut|pussy|porn|ashawo|olosho)' then
    raise exception 'Please pick a different name.';
  end if;
  if (select count(*) from public.landings where created_at > now() - interval '1 minute') >= 20 then
    raise exception 'The board is busy. Try again in a minute.';
  end if;
  if new.name <> 'Anonymous lander'
     and (select count(*) from public.landings where name = new.name and created_at > now() - interval '1 hour') >= 20 then
    raise exception 'That name has posted a lot this hour.';
  end if;
  return new;
end $$;

drop trigger if exists landings_guard on public.landings;
create trigger landings_guard before insert on public.landings
  for each row execute function public.landings_guard();
