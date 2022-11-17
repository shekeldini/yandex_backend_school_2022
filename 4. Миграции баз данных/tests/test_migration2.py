import os

from _pytest.outcomes import fail
from sqlalchemy import MetaData, create_engine
import sqlalchemy as alchemy
from sqlalchemy.orm import Session, declarative_base

from MigrationsHelper import MigrationsHelper
from tests.entities.Driver import DriverV1, get_drivers_v1_from_csv
from tests.entities.Spaceship import Spaceship, get_spaceships_from_csv
from tests.entities.SpaceshipManufacturer import SpaceshipManufacturerV1, get_spaceship_manufacturers_v1_from_csv
from tests.entities.SpaceshipModel import SpaceshipModel, get_spaceship_models_from_csv
from tests.entities.SpaceshipRent import SpaceshipRent, get_spaceship_rent_from_csv


def setup():
    os.environ['SDB_TRACK'] = 'python'


def test_migration_2_smoke():
    MigrationsHelper.update(2)
    MigrationsHelper.rollback(2)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)
    assert len(meta_data.tables) <= 2


def test_migration_2_driver_content():
    MigrationsHelper.update(2)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)

    drivers_from_csv = get_drivers_v1_from_csv()

    with Session(MigrationsHelper.db) as session:
        for driver_from_db in session.query(DriverV1).all():
            if driver_from_db in drivers_from_csv:
                drivers_from_csv.remove(driver_from_db)
            else:
                fail()

    assert len(drivers_from_csv) == 0
    MigrationsHelper.rollback(2)


def test_migration_2_spaceship_manufacturer_content():
    MigrationsHelper.update(2)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)

    manufacturers_from_csv = get_spaceship_manufacturers_v1_from_csv()

    with Session(MigrationsHelper.db) as session:
        for manufacturer_from_db in session.query(SpaceshipManufacturerV1).all():
            if manufacturer_from_db in manufacturers_from_csv:
                manufacturers_from_csv.remove(manufacturer_from_db)
            else:
                fail()

    assert len(manufacturers_from_csv) == 0
    MigrationsHelper.rollback(2)


def test_migration_2_spaceship_model_content():
    MigrationsHelper.update(2)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)

    spaceship_models_from_csv = get_spaceship_models_from_csv()

    with Session(MigrationsHelper.db) as session:
        for spaceship_model_from_db in session.query(SpaceshipModel).all():
            if spaceship_model_from_db in spaceship_models_from_csv:
                spaceship_models_from_csv.remove(spaceship_model_from_db)
            else:
                fail()

    assert len(spaceship_models_from_csv) == 0
    MigrationsHelper.rollback(2)


def test_migration_2_spaceship_content():
    MigrationsHelper.update(2)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)

    spaceships_from_csv = get_spaceships_from_csv()

    with Session(MigrationsHelper.db) as session:
        for spaceship_from_db in session.query(Spaceship).all():
            if spaceship_from_db in spaceships_from_csv:
                spaceships_from_csv.remove(spaceship_from_db)
            else:
                fail()

    assert len(spaceships_from_csv) == 0
    MigrationsHelper.rollback(2)


def test_migration_2_spaceship_rent_content():
    MigrationsHelper.update(2)
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)

    spaceship_rents_from_csv = get_spaceship_rent_from_csv()

    with Session(MigrationsHelper.db) as session:
        for spaceship_rent_from_db in session.query(SpaceshipRent).all():
            if spaceship_rent_from_db in spaceship_rents_from_csv:
                spaceship_rents_from_csv.remove(spaceship_rent_from_db)
            else:
                fail()

    assert len(spaceship_rents_from_csv) == 0
    MigrationsHelper.rollback(2)

