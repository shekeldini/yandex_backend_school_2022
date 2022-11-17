-- Укажите дополнительные индексы
create index v1_idx_1 on users_user (upper(id::text));
create index v1_idx_2 on users_user using gin (upper(first_name) gin_trgm_ops, upper(last_name) gin_trgm_ops);
