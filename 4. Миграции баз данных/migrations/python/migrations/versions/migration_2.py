"""empty message

Revision ID: 60feda05ef56
Revises: 2519a08b90aa
Create Date: 2022-08-07 11:48:23.001390

"""
from alembic import op
from sqlalchemy import and_, MetaData, Table, delete, Column, VARCHAR, INTEGER, TIMESTAMP
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

# revision identifiers, used by Alembic.
revision = '60feda05ef56'
down_revision = 'c43b5e3e04d4'
branch_labels = None
depends_on = None

Meta = MetaData(bind=op.get_bind())

driver = Table(
    'driver',
    Meta,
    Column('id', INTEGER, primary_key=True),
    Column('name', VARCHAR(50), nullable=False),
    Column('last_name', VARCHAR(50), nullable=False),
    Column('login', VARCHAR(50), unique=True, nullable=False),
    Column('city', VARCHAR(30), nullable=True)
)

spaceship = Table(
    'spaceship',
    Meta,
    Column('id', INTEGER, primary_key=True),
    Column('ship_number', VARCHAR(50), nullable=False),
    Column('model_id', INTEGER, nullable=True)
)
spaceship_manufacturer = Table(
    'spaceship_manufacturer',
    Meta,
    Column('id', INTEGER, primary_key=True),
    Column('company_name', VARCHAR(50), nullable=False),
    Column('country', VARCHAR(50), nullable=True),
    Column('nasdaq_code', VARCHAR(50), nullable=True)
)

spaceship_model = Table(
    'spaceship_model',
    Meta,
    Column('id', INTEGER, primary_key=True),
    Column('manufacturer_id', INTEGER, nullable=False),
    Column('model_name', VARCHAR(50), nullable=True),
    Column('horsepower', DOUBLE_PRECISION, nullable=False)
)

spaceship_rent = Table(
    'spaceship_rent',
    Meta,
    Column('driver_id', INTEGER, nullable=False, primary_key=True),
    Column('spaceship_id', INTEGER, nullable=False, primary_key=True),
    Column('rent_start', TIMESTAMP, nullable=False),
    Column('rent_end', TIMESTAMP, nullable=False)
)


def upgrade() -> None:
    Meta.reflect(only=(
        'spaceship_rent',
        'spaceship_model',
        'spaceship_manufacturer',
        'spaceship',
        'driver'
    ))
    op.bulk_insert(
        spaceship_manufacturer,
        [
            {"id": 1, "company_name": "Ford Nuclear Engine", "country": "USA", "nasdaq_code": "frdne"},
            {"id": 2, "company_name": "Cosmical Motors", "country": "USA", "nasdaq_code": "cosmot"},
            {"id": 3, "company_name": "Автокосмоваз", "country": "RU", "nasdaq_code": "acaz"},
            {"id": 4, "company_name": "BNW", "country": "GE", "nasdaq_code": "bnw"},
        ]
    )
    op.bulk_insert(
        spaceship_model,
        [
            {"id": 1, "manufacturer_id": 1, "model_name": "Aerostar", "horsepower": 170135000},
            {"id": 2, "manufacturer_id": 2, "model_name": "Stardilac", "horsepower": 175000000},
            {"id": 3, "manufacturer_id": 3, "model_name": "Lada Moonta", "horsepower": 240000000},
            {"id": 4, "manufacturer_id": 4, "model_name": "X5000", "horsepower": 190000000},
        ]
    )
    op.bulk_insert(
        spaceship,
        [
            {"id": 1, "ship_number": "A300BC 177", "model_id": 3},
            {"id": 2, "ship_number": "A245BC 177", "model_id": 1},
            {"id": 3, "ship_number": "A412RE 76", "model_id": 2},
            {"id": 4, "ship_number": "X078BA 76", "model_id": 4},
        ]
    )
    op.bulk_insert(
        driver,
        [
            {"id": 1, "name": "Arcady", "last_name": "Volozh", "login": "volozh.a", "city": "Moscow"},
            {"id": 2, "name": "Lena", "last_name": "Bunina", "login": "bunina.e", "city": "Tel-Aviv"},
            {"id": 3, "name": "David", "last_name": "Patterson", "login": "patterson.d", "city": "Berkeley"},
            {"id": 4, "name": "James", "last_name": "Gosling", "login": "gosling.j", "city": "San José"},
            {"id": 5, "name": "Elon", "last_name": "Musk", "login": "elon", "city": "Boca Chica Village"},
        ]
    )
    op.bulk_insert(
        spaceship_rent,
        [
            {"driver_id": 1, "spaceship_id": 3, "rent_start": "2059-07-25 11:13:54", "rent_end": "2059-09-30 11:14:04"},
            {"driver_id": 2, "spaceship_id": 4, "rent_start": "2060-06-24 11:14:23", "rent_end": "2064-07-31 11:14:35"},
            {"driver_id": 3, "spaceship_id": 2, "rent_start": "2055-12-24 11:14:55", "rent_end": "2061-11-01 11:15:05"},
            {"driver_id": 4, "spaceship_id": 1, "rent_start": "2059-12-31 11:15:27", "rent_end": "2060-02-29 11:15:36"},
            {"driver_id": 5, "spaceship_id": 3, "rent_start": "2022-07-15 11:23:35", "rent_end": "2059-07-31 11:23:46"},
        ]
    )


def downgrade() -> None:
    # SpaceshipRent
    op.execute(delete(spaceship_rent).where(
        and_(
            spaceship_rent.c.driver_id == 1,
            spaceship_rent.c.spaceship_id == 3,
            spaceship_rent.c.rent_start == "2059-07-25 11:13:54",
            spaceship_rent.c.rent_end == "2059-09-30 11:14:04",
        )
    )
    )
    op.execute(delete(spaceship_rent).where(
        and_(
            spaceship_rent.c.driver_id == 2,
            spaceship_rent.c.spaceship_id == 4,
            spaceship_rent.c.rent_start == "2060-06-24 11:14:23",
            spaceship_rent.c.rent_end == "2064-07-31 11:14:35",
        )
    )
    )
    op.execute(delete(spaceship_rent).where(
        and_(
            spaceship_rent.c.driver_id == 3,
            spaceship_rent.c.spaceship_id == 2,
            spaceship_rent.c.rent_start == "2055-12-24 11:14:55",
            spaceship_rent.c.rent_end == "2061-11-01 11:15:05",
        )
    )
    )
    op.execute(delete(spaceship_rent).where(
        and_(
            spaceship_rent.c.driver_id == 4,
            spaceship_rent.c.spaceship_id == 1,
            spaceship_rent.c.rent_start == "2059-12-31 11:15:27",
            spaceship_rent.c.rent_end == "2060-02-29 11:15:36",
        )
    )
    )
    op.execute(delete(spaceship_rent).where(
        and_(
            spaceship_rent.c.driver_id == 5,
            spaceship_rent.c.spaceship_id == 3,
            spaceship_rent.c.rent_start == "2022-07-15 11:23:35",
            spaceship_rent.c.rent_end == "2059-07-31 11:23:46",
        )
    )
    )

    # Driver
    op.execute(delete(driver).where(driver.c.id.in_([1, 2, 3, 4, 5])))
    # Spaceship
    op.execute(delete(spaceship).where(spaceship.c.id.in_([1, 2, 3, 4])))
    # SpaceshipModel
    op.execute(delete(spaceship_model).where(spaceship_model.c.id.in_([1, 2, 3, 4])))
    # SpaceshipManufacturer
    op.execute(delete(spaceship_manufacturer).where(spaceship_manufacturer.c.id.in_([1, 2, 3, 4])))
