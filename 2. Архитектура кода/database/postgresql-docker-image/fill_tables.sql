COPY specialty (name) FROM '/specialties.txt';
COPY common_item (
	name,
	amount,
	price,
	dosage_form,
	manufacturer,
	barcode
) FROM '/generated_data/common_items.csv' DELIMITER ',' CSV HEADER;
COPY receipt_item (
	name,
	amount,
	price,
	dosage_form,
	manufacturer,
	barcode
) FROM '/generated_data/receipt_items.csv' DELIMITER ',' CSV HEADER;
COPY user_account (
	full_name,
	phone,
	password_hash,
    id
) FROM '/generated_data/users.csv' DELIMITER ',' CSV HEADER;

CREATE TEMPORARY TABLE temp_special_item (
	name text,
	amount integer,
	price numeric(8, 2),
	dosage_form text,
	manufacturer text,
	barcode text UNIQUE,
	specialty text
);
COPY temp_special_item FROM '/generated_data/special_items.csv' DELIMITER ',' CSV HEADER;
INSERT INTO special_item (
	name,
	amount,
	price,
	dosage_form,
	manufacturer,
	barcode,
	specialty_id
) SELECT
	temp_special_item.name AS name,
	temp_special_item.amount AS amount,
	temp_special_item.price AS price,
	temp_special_item.dosage_form AS dosage_form,
	temp_special_item.manufacturer AS manufacturer,
	temp_special_item.barcode AS barcode,
	specialty.id AS specialty_id
FROM temp_special_item
JOIN specialty ON temp_special_item.specialty = specialty.name;

CREATE TEMPORARY TABLE temp_doctor_account (
	full_name text,
	phone text UNIQUE,
	password_hash text,
	specialty text,
	id integer
);
COPY temp_doctor_account FROM '/generated_data/doctors.csv' DELIMITER ',' CSV HEADER;
INSERT INTO doctor_account (
	full_name,
	phone,
	password_hash,
	specialty_id,
    id
) SELECT
	temp_doctor_account.full_name AS full_name,
	temp_doctor_account.phone AS phone,
	temp_doctor_account.password_hash AS password_hash,
	specialty.id AS specialty_id,
    temp_doctor_account.id as id
FROM temp_doctor_account
JOIN specialty ON temp_doctor_account.specialty = specialty.name;

CREATE TEMPORARY TABLE temp_receipt (
	phone text,
	barcode text,
	UNIQUE (phone, barcode)
);
COPY temp_receipt FROM '/generated_data/receipts.csv' DELIMITER ',' CSV HEADER;
INSERT INTO receipt (
	user_id,
	item_id
) SELECT
	user_account.id AS user_id,
	receipt_item.id AS item_id
FROM temp_receipt
JOIN user_account ON temp_receipt.phone = user_account.phone
JOIN receipt_item ON temp_receipt.barcode = receipt_item.barcode;
