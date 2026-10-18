-- Car Scout tables. Run this once in the Supabase dashboard: SQL Editor > New query > paste > Run.
-- It is safe to run again: existing tables and their rows are kept.

-- One row per user, updated every time the user asks for something new.
create table if not exists public.user_preferences (
    user_id text primary key,
    preferred_brand text,
    preferred_transmission text,
    max_price_tnd integer,
    preferred_city text,
    preferred_fuel text,
    favorite_models text[] not null default '{}',
    updated_at timestamptz not null default now()
);

-- One row per message. All messages of one chat share the same conversation_id.
create table if not exists public.conversation_messages (
    id bigint generated always as identity primary key,
    conversation_id uuid not null,
    user_id text not null,
    role text not null check (role in ('user', 'assistant')),
    content text not null,
    created_at timestamptz not null default now()
);

create index if not exists conversation_messages_conversation_idx
    on public.conversation_messages (conversation_id, id);

-- Row level security with no policies: the publishable key cannot read or write these tables.
-- Only the secret key (SUPABASE_SECRET_KEY in .env) can.
alter table public.user_preferences enable row level security;
alter table public.conversation_messages enable row level security;

grant select, insert, update on public.user_preferences to service_role;
grant select, insert, update on public.conversation_messages to service_role;
