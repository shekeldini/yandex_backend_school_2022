import os

from _pytest.outcomes import fail
from sqlalchemy import MetaData, create_engine, Column, Table
import sqlalchemy as alchemy
from sqlalchemy.orm import Session

from MigrationsHelper import MigrationsHelper
from tests.entities.DriverV2 import get_drivers_v2_from_csv, DriverV2
from tests.entities.SpaceshipManufacturerV2 import SpaceshipManufacturerV2, get_spaceship_manufacturers_v2_from_csv


def setup():
    os.environ['SDB_TRACK'] = 'python'


def test_migration_3_smoke():
    MigrationsHelper.update(3)
    MigrationsHelper.rollback(3)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)
    assert len(meta_data.tables) <= 2


def test_migration_3_spaceship_manufacturer_structure():
    MigrationsHelper.update(3)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)

    manufacturer_table: Table = meta_data.tables['spaceship_manufacturer']
    assert 'moex_code' in manufacturer_table.columns.keys()
    assert 'nasdaq_code' not in manufacturer_table.columns.keys()
    MigrationsHelper.rollback(3)


def test_migration_3_spaceship_manufacturer_content():
    MigrationsHelper.update(3)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)

    manufacturers_from_csv = get_spaceship_manufacturers_v2_from_csv()

    with Session(MigrationsHelper.db) as session:
        for manufacturer_from_db in session.query(SpaceshipManufacturerV2).all():
            if manufacturer_from_db in manufacturers_from_csv:
                manufacturers_from_csv.remove(manufacturer_from_db)
            else:
                fail()

    assert len(manufacturers_from_csv) == 0
    MigrationsHelper.rollback(3)


def test_migration_3_driver_structure():
    MigrationsHelper.update(3)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)

    driver_table: Table = meta_data.tables['driver']
    assert 'full_name' in driver_table.columns.keys()
    assert 'name' not in driver_table.columns.keys()
    assert 'last_name' not in driver_table.columns.keys()
    MigrationsHelper.rollback(3)


def test_migration_3_driver_content():
    MigrationsHelper.update(3)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)

    drivers_from_csv = get_drivers_v2_from_csv()

    with Session(MigrationsHelper.db) as session:
        for driver_from_db in session.query(DriverV2).all():
            if driver_from_db in drivers_from_csv:
                drivers_from_csv.remove(driver_from_db)
            else:
                fail()

    assert len(drivers_from_csv) == 0
    MigrationsHelper.rollback(3)