alter table users_user add column users_company_title text;
alter table users_user add column users_job_title text;
alter table users_user add column fio text;

UPDATE users_user SET users_company_title = (SELECT title FROM users_company WHERE users_user.company_id = users_company.id);
UPDATE users_user SET users_job_title = (SELECT title FROM users_job WHERE users_user.job_id = users_job.id);
UPDATE users_user SET fio = last_name || ' ' || first_name || ' ' || second_name;

create index v3_idx_1 on users_user (upper(id::text));
create index v3_idx_2 on users_user using gin (
upper(first_name) gin_trgm_ops,
upper(second_name) gin_trgm_ops,
upper(last_name) gin_trgm_ops,
upper(phone_number) gin_trgm_ops,
upper(email) gin_trgm_ops,
upper(fio) gin_trgm_ops,
upper(users_company_title) gin_trgm_ops,
upper(users_job_title) gin_trgm_ops
);
create index v3_idx_3 on users_user (fio ASC);

SELECT  
 "users_user"."id",  
 "users_user"."first_name",  
 "users_user"."second_name",  
 "users_user"."last_name",  
 "users_user"."email",  
 "users_user"."address",  
 "users_user"."phone_number",  
 "users_user"."company_id",  
 "users_user"."job_id",  
 "users_user"."fio"  
FROM "users_user"
WHERE ( 
 UPPER("users_user"."id"::text) = UPPER('Иван') OR  
 UPPER("users_user"."first_name"::text) LIKE UPPER('Иван%') OR  
 UPPER("users_user"."last_name"::text) LIKE UPPER('%Иван%') OR  
 UPPER("users_user"."second_name"::text) LIKE UPPER('%Иван%') OR  
 UPPER("users_user"."phone_number"::text) LIKE UPPER('%Иван%') OR
 UPPER(fio) LIKE UPPER('%Иван%') OR
 UPPER("users_user"."email"::text) LIKE UPPER('%Иван%') OR
 UPPER(users_company_title) like UPPER('%Иван%') OR
 UPPER(users_job_title) like UPPER('%Иван%')
) ORDER BY "fio" ASC;
