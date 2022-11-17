CREATE TABLE IF NOT EXISTS specialty(
	id integer primary key generated always as identity,
	name text UNIQUE
);

CREATE TABLE IF NOT EXISTS common_item (
	id integer primary key generated always as identity,
	name text,
	amount integer,
	price numeric(8, 2),
	dosage_form text,
	manufacturer text,
	barcode text UNIQUE
);

CREATE TABLE IF NOT EXISTS special_item (
	id integer primary key generated always as identity,
	name text,
	amount integer,
	price numeric(8, 2),
	dosage_form text,
	manufacturer text,
	barcode text UNIQUE,
	specialty_id integer references specialty(id)
);

CREATE TABLE IF NOT EXISTS receipt_item (
	id integer primary key generated always as identity,
	name text,
	amount integer,
	price numeric(8, 2),
	dosage_form text,
	manufacturer text,
	barcode text UNIQUE
);

CREATE TABLE IF NOT EXISTS user_account (
	id integer primary key,
	full_name text,
	phone text UNIQUE,
	password_hash text
);

CREATE TABLE IF NOT EXISTS doctor_account (
	id integer primary key,
	full_name text,
	phone text UNIQUE,
	password_hash text,
	specialty_id integer references specialty(id)
);

CREATE TABLE IF NOT EXISTS receipt (
	id integer primary key generated always as identity,
	user_id integer references user_account(id),
	item_id integer references receipt_item(id),
	UNIQUE (user_id, item_id)
);
