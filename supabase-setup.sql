-- ============================================================
--  Supabase Setup for Portfolio Contact Form
--  Run this in: Supabase Dashboard → SQL Editor → New Query
-- ============================================================

-- 1. Create the contact_messages table
create table if not exists contact_messages (
  id         uuid        primary key default gen_random_uuid(),
  name       text        not null,
  email      text        not null,
  subject    text        not null,
  message    text        not null,
  created_at timestamptz not null default now()
);

-- 2. Enable Row Level Security (RLS)
alter table contact_messages enable row level security;

-- 3. Allow anyone (anon) to INSERT — no login required from the portfolio visitor
create policy "Allow public inserts"
  on contact_messages
  for insert
  to anon
  with check (true);

-- 4. Restrict SELECT / UPDATE / DELETE to authenticated users only
--    (so only you can read submissions via the Supabase dashboard or your own admin UI)
create policy "Allow authenticated reads"
  on contact_messages
  for select
  to authenticated
  using (true);

-- (Optional) Index on created_at for efficient ordering
create index if not exists idx_contact_messages_created_at
  on contact_messages (created_at desc);
