-- ============================================================
-- Learning Tracker — 用户配对 / 日程共享 迁移
-- 在 Supabase SQL Editor 里执行一次即可。幂等写法，重复执行不会出错。
-- ============================================================

-- ── 1. profiles 表：保存 user_id ↔ username 映射，用于按用户名查找配对对象。
--     所有已登录用户都能查（用于 username 搜索），但只能写自己的。
create table if not exists learning_tracker_profiles (
  user_id      uuid primary key references auth.users(id) on delete cascade,
  username     text unique not null,
  display_name text,
  created_at   timestamptz default now(),
  updated_at   timestamptz default now()
);

alter table learning_tracker_profiles enable row level security;

drop policy if exists "profiles_read_authed" on learning_tracker_profiles;
create policy "profiles_read_authed" on learning_tracker_profiles
  for select using (auth.role() = 'authenticated');

drop policy if exists "profiles_insert_self" on learning_tracker_profiles;
create policy "profiles_insert_self" on learning_tracker_profiles
  for insert with check (auth.uid() = user_id);

drop policy if exists "profiles_update_self" on learning_tracker_profiles;
create policy "profiles_update_self" on learning_tracker_profiles
  for update using (auth.uid() = user_id);


-- ── 2. pairs 表：配对关系。
--     状态机：pending → accepted | declined。同一对用户之间只能有一条 active 关系。
--     双方都能 SELECT/UPDATE（接受、解除），只有发起方能 INSERT。
create table if not exists learning_tracker_pairs (
  id                  uuid primary key default gen_random_uuid(),
  requester_id        uuid not null references auth.users(id) on delete cascade,
  partner_id          uuid not null references auth.users(id) on delete cascade,
  requester_username  text not null,
  partner_username    text not null,
  status              text not null check (status in ('pending', 'accepted', 'declined')),
  created_at          timestamptz default now(),
  updated_at          timestamptz default now(),
  constraint pairs_no_self check (requester_id <> partner_id)
);

-- Active 关系唯一（partial unique 在 pending+accepted 上）
create unique index if not exists pairs_active_unique
  on learning_tracker_pairs (least(requester_id, partner_id), greatest(requester_id, partner_id))
  where status in ('pending', 'accepted');

alter table learning_tracker_pairs enable row level security;

drop policy if exists "pairs_select_involved" on learning_tracker_pairs;
create policy "pairs_select_involved" on learning_tracker_pairs
  for select using (auth.uid() = requester_id or auth.uid() = partner_id);

drop policy if exists "pairs_insert_as_requester" on learning_tracker_pairs;
create policy "pairs_insert_as_requester" on learning_tracker_pairs
  for insert with check (auth.uid() = requester_id);

drop policy if exists "pairs_update_involved" on learning_tracker_pairs;
create policy "pairs_update_involved" on learning_tracker_pairs
  for update using (auth.uid() = requester_id or auth.uid() = partner_id);

drop policy if exists "pairs_delete_involved" on learning_tracker_pairs;
create policy "pairs_delete_involved" on learning_tracker_pairs
  for delete using (auth.uid() = requester_id or auth.uid() = partner_id);


-- ── 3. learning_tracker_data 增加策略：accepted 配对的伴侣可读对方那一行。
--     原有「自己读写自己」的策略保持不变；这里只新增一条「伴侣可读」。
drop policy if exists "data_read_accepted_partner" on learning_tracker_data;
create policy "data_read_accepted_partner" on learning_tracker_data
  for select using (
    exists (
      select 1 from learning_tracker_pairs p
      where p.status = 'accepted'
        and (
          (p.requester_id = auth.uid() and p.partner_id = learning_tracker_data.user_id)
          or
          (p.partner_id  = auth.uid() and p.requester_id = learning_tracker_data.user_id)
        )
    )
  );


-- ── 4. （可选，但推荐）触发器：updated_at 自动更新
create or replace function set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists profiles_set_updated on learning_tracker_profiles;
create trigger profiles_set_updated
  before update on learning_tracker_profiles
  for each row execute function set_updated_at();

drop trigger if exists pairs_set_updated on learning_tracker_pairs;
create trigger pairs_set_updated
  before update on learning_tracker_pairs
  for each row execute function set_updated_at();
