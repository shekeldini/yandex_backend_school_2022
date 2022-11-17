import csv
import random
import typing
from decimal import Decimal
from pathlib import Path

from mimesis import Person
from mimesis import Schema
from mimesis.locales import Locale
from mimesis.types import CallableSchema
from mimesis.types import JSON


# Список лекарственных препаратов взят с https://minzdrav.gov.ru/opendata
MEDICINES_FILENAME = "data-20160926T0000-structure-20150610T0000.csv"
SPECIALTIES_FILENAME = "specialties.txt"


def get_filepath(filename: str) -> Path:
    return Path(__file__).parent.resolve() / filename


def create_filepath(filename: str) -> Path:
    parent = Path(__file__).parent.resolve() / "generated_data"
    parent.mkdir(exist_ok=True)
    return parent / filename


def write_to_csv(filename: str, rows: typing.Sequence[JSON]) -> None:
    if not rows:
        raise ValueError("No rows")

    fieldnames = rows[0].keys()
    with open(create_filepath(filename), "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def get_user_schema(provider: Person, *, doctor: bool = False) -> CallableSchema:
    def generate_user() -> JSON:
        user = {
            "full_name": provider.full_name(),
            "phone": provider.telephone(),
            "password_hash": provider.password(hashed=True),
        }
        if doctor:
            user["specialty"] = random.choice(specialties)
        return user

    return generate_user


if __name__ == "__main__":
    with open(get_filepath(SPECIALTIES_FILENAME)) as txtfile:
        specialties = txtfile.read().splitlines()

    barcodes = set()
    common_items = []
    special_items = []
    receipt_items = []
    with open(get_filepath(MEDICINES_FILENAME)) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["barcode"] in barcodes:
                continue

            date = row["registrationdate"].split()[0]
            item = {
                "name": "".join(char for char in row["tradename"] if char not in "(*)"),
                "amount": int(row["amount"].replace(" ", "")),
                "price": Decimal(row["limitingprice"].replace(" ", "")),
                "dosage_form": row["dosageform"].strip(),
                "manufacturer": row["manufacturer"],
                "barcode": row["barcode"],
            }
            probability = random.random()
            if probability < 1 / 3:
                item["specialty"] = random.choice(specialties)
                special_items.append(item)
            elif probability < 2 / 3:
                receipt_items.append(item)
            else:
                common_items.append(item)

            barcodes.add(row["barcode"])

    write_to_csv("common_items.csv", common_items)
    write_to_csv("special_items.csv", special_items)
    write_to_csv("receipt_items.csv", receipt_items)

    person = Person(locale=Locale.RU)

    receipts = []
    user_schema = Schema(get_user_schema(person))
    users = user_schema.create(iterations=40)
    for user in user_schema.iterator(iterations=20):
        users.append(user)
        for item in random.sample(receipt_items, random.randint(1, 3)):
            receipt = {"user_phone": user["phone"], "item_barcode": item["barcode"]}
            receipts.append(receipt)

    write_to_csv("users.csv", users)
    write_to_csv("receipts.csv", receipts)

    doctor_schema = Schema(get_user_schema(person, doctor=True))
    doctor_schema.to_csv(create_filepath("doctors.csv"), iterations=40)
