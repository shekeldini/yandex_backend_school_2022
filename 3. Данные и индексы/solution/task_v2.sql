-- Укажите дополнительные индексы и команды

create index v2_idx_1 on users_user (upper(id::text));

create index v2_idx_2 on users_user using gin (
upper(first_name) gin_trgm_ops,
upper(last_name) gin_trgm_ops,
upper(phone_number) gin_trgm_ops,
upper(email) gin_trgm_ops
);

create index v2_idx_3 on users_user (last_name ASC);
