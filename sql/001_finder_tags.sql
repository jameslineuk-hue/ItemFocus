-- Run this in the Supabase SQL editor (or via migrations) before first deploy.

create extension if not exists "pgcrypto";

create table if not exists public.finder_tags (
  id uuid primary key default gen_random_uuid(),
  public_code text not null unique,
  category text not null check (category in ('laptop', 'keys', 'wallet', 'other')),
  owner_name text not null,
  owner_phone text not null,
  created_at timestamptz not null default now()
);

create index if not exists finder_tags_public_code_idx on public.finder_tags (public_code);

comment on table public.finder_tags is 'ItemFocus QR tags linking a public code to owner contact details.';
comment on column public.finder_tags.public_code is 'Printed on the tag, e.g. IF-AB12CD';
comment on column public.finder_tags.category is 'Item type for finder context';

alter table public.finder_tags enable row level security;

-- Intentionally no policies: use the service role key only from the Python API (never in the browser).
