import os
from datetime import datetime

import pytest

from MigrationsHelper import MigrationsHelper
from sqlalchemy import create_engine, Table, Column, UniqueConstraint, CheckConstraint
from sqlalchemy import MetaData
import sqlalchemy as alchemy


def setup():
    os.environ['SDB_TRACK'] = 'python'


class TestMigration1:
    def test_migration_1_tables(self):
        MigrationsHelper.update(1)
        meta_data = MetaData(bind=MigrationsHelper.db)
        alchemy.MetaData.reflect(meta_data)

        assert 'driver' in meta_data.tables.keys()
        assert 'spaceship_rent' in meta_data.tables.keys()
        assert 'spaceship' in meta_data.tables.keys()
        assert 'spaceship_model' in meta_data.tables.keys()
        assert 'spaceship_manufacturer' in meta_data.tables.keys()

        MigrationsHelper.rollback(1)
        meta_data = MetaData(bind=MigrationsHelper.db)
        alchemy.MetaData.reflect(meta_data)

        assert len(meta_data.tables) <= 2

    def test_migration_1_driver_columns_list(self):
        MigrationsHelper.update(1)
        meta_data = MetaData(bind=MigrationsHelper.db)
        alchemy.MetaData.reflect(meta_data)

        driver_table: Table = meta_data.tables['driver']
        assert 'id' in driver_table.columns.keys()
        assert 'name' in driver_table.columns.keys()
        assert 'last_name' in driver_table.columns.keys()
        assert 'login' in driver_table.columns.keys()
        assert 'city' in driver_table.columns.keys()

        MigrationsHelper.rollback(1)

    def test_migration_1_driver_columns_properties(self):
        MigrationsHelper.update(1)
        meta_data = MetaData(bind=MigrationsHelper.db)
        alchemy.MetaData.reflect(meta_data)

        driver_table: Table = meta_data.tables['driver']
        id_column: Column = driver_table.columns['id']
        assert id_column.type.python_type == int
        assert id_column.primary_key
        assert len(id_column.foreign_keys) == 0
        assert not id_column.nullable

        name_column: Column = driver_table.columns['name']
        assert name_column.type.python_type == str
        assert name_column.type.length == 50
        assert not name_column.primary_key
        assert len(name_column.foreign_keys) == 0
        assert not name_column.nullable

        last_name_column: Column = driver_table.columns['last_name']
        assert last_name_column.type.python_type == str
        assert last_name_column.type.length == 50
        assert not last_name_column.primary_key
        assert len(last_name_column.foreign_keys) == 0
        assert last_name_column.nullable

        login_column: Column = driver_table.columns['login']
        assert login_column.type.python_type == str
        assert login_column.type.length == 50
        assert not login_column.primary_key
        assert len(login_column.foreign_keys) == 0
        assert not login_column.nullable

        city_column: Column = driver_table.columns['city']
        assert city_column.type.python_type == str
        assert city_column.type.length == 30
        assert not city_column.primary_key
        assert len(city_column.foreign_keys) == 0
        assert city_column.nullable

        unique_login_columns = [
            column for constraint in driver_table.constraints for column in constraint.columns
            if type(constraint) == UniqueConstraint and column.name == 'login'
        ]
        assert len(unique_login_columns) >= 1
        MigrationsHelper.rollback(1)

    def test_migration_1_spaceship_manufacturer_column_properties(self):
        MigrationsHelper.update(1)
        meta_data = MetaData(bind=MigrationsHelper.db)
        alchemy.MetaData.reflect(meta_data)

        spaceship_manufacturer_table: Table = meta_data.tables['spaceship_manufacturer']
        id_column: Column = spaceship_manufacturer_table.columns['id']
        assert id_column.type.python_type == int
        assert id_column.primary_key
        assert len(id_column.foreign_keys) == 0
        assert not id_column.nullable

        company_name_column: Column = spaceship_manufacturer_table.columns['company_name']
        assert company_name_column.type.python_type == str
        assert company_name_column.type.length == 50
        assert not company_name_column.primary_key
        assert len(company_name_column.foreign_keys) == 0
        assert not company_name_column.nullable

        country_column: Column = spaceship_manufacturer_table.columns['country']
        assert country_column.type.python_type == str
        assert country_column.type.length == 50
        assert not country_column.primary_key
        assert len(country_column.foreign_keys) == 0
        assert country_column.nullable

        nasdaq_column: Column = spaceship_manufacturer_table.columns['nasdaq_code']
        assert nasdaq_column.type.python_type == str
        assert nasdaq_column.type.length == 50
        assert not nasdaq_column.primary_key
        assert len(nasdaq_column.foreign_keys) == 0
        assert nasdaq_column.nullable

        MigrationsHelper.rollback(1)

    def test_migration_1_spaceship_model_column_properties(self):
        MigrationsHelper.update(1)
        meta_data = MetaData(bind=MigrationsHelper.db)
        alchemy.MetaData.reflect(meta_data)

        spaceship_manufacturer_table: Table = meta_data.tables['spaceship_model']
        id_column: Column = spaceship_manufacturer_table.columns['id']
        assert id_column.type.python_type == int
        assert id_column.primary_key
        assert len(id_column.foreign_keys) == 0
        assert not id_column.nullable

        manufacturer_id_column: Column = spaceship_manufacturer_table.columns['manufacturer_id']
        assert manufacturer_id_column.type.python_type == int
        assert not manufacturer_id_column.primary_key
        assert len(manufacturer_id_column.foreign_keys) == 1
        fk = list(manufacturer_id_column.foreign_keys)[0]
        assert fk.column.table.name == 'spaceship_manufacturer'
        assert fk.column.name == 'id'
        assert not manufacturer_id_column.nullable

        model_name_column: Column = spaceship_manufacturer_table.columns['model_name']
        assert model_name_column.type.python_type == str
        assert model_name_column.type.length == 50
        assert not model_name_column.primary_key
        assert len(model_name_column.foreign_keys) == 0
        assert model_name_column.nullable

        horsepower_column: Column = spaceship_manufacturer_table.columns['horsepower']
        assert horsepower_column.type.python_type == float
        assert not horsepower_column.primary_key
        assert len(horsepower_column.foreign_keys) == 0
        assert not horsepower_column.nullable

        check_constraints = [
            constraint for constraint in spaceship_manufacturer_table.constraints
            if type(constraint) == CheckConstraint and
               any(check_part in constraint.sqltext.text for check_part in ['horsepower', '170000000', '240000000'])
        ]

        assert len(check_constraints) > 0

        MigrationsHelper.rollback(1)

    def test_migration_1_spaceship_column_properties(self):
        MigrationsHelper.update(1)
        meta_data = MetaData(bind=MigrationsHelper.db)
        alchemy.MetaData.reflect(meta_data)

        spaceship_table: Table = meta_data.tables['spaceship']
        id_column: Column = spaceship_table.columns['id']
        assert id_column.type.python_type == int
        assert id_column.primary_key
        assert len(id_column.foreign_keys) == 0
        assert not id_column.nullable

        model_id_column: Column = spaceship_table.columns['model_id']
        assert model_id_column.type.python_type == int
        assert not model_id_column.primary_key
        assert len(model_id_column.foreign_keys) == 1
        fk = list(model_id_column.foreign_keys)[0]
        assert fk.column.table.name == 'spaceship_model'
        assert fk.column.name == 'id'
        assert not model_id_column.nullable

        ship_number_column: Column = spaceship_table.columns['ship_number']
        assert ship_number_column.type.python_type == str
        assert ship_number_column.type.length == 50
        assert not ship_number_column.primary_key
        assert len(ship_number_column.foreign_keys) == 0
        assert not ship_number_column.nullable

        MigrationsHelper.rollback(1)

    def test_migration_1_spaceship_rent_column_properties(self):
        MigrationsHelper.update(1)
        meta_data = MetaData(bind=MigrationsHelper.db)
        alchemy.MetaData.reflect(meta_data)

        spaceship_rent_table: Table = meta_data.tables['spaceship_rent']
        driver_id_column: Column = spaceship_rent_table.columns['driver_id']
        assert driver_id_column.type.python_type == int
        assert not driver_id_column.primary_key
        assert len(driver_id_column.foreign_keys) == 1
        fk = list(driver_id_column.foreign_keys)[0]
        assert fk.column.table.name == 'driver'
        assert fk.column.name == 'id'
        assert not driver_id_column.nullable

        spaceship_id_column: Column = spaceship_rent_table.columns['spaceship_id']
        assert spaceship_id_column.type.python_type == int
        assert not spaceship_id_column.primary_key
        assert len(spaceship_id_column.foreign_keys) == 1
        fk = list(spaceship_id_column.foreign_keys)[0]
        assert fk.column.table.name == 'spaceship'
        assert fk.column.name == 'id'
        assert not spaceship_id_column.nullable

        rent_start_column: Column = spaceship_rent_table.columns['rent_start']
        assert rent_start_column.type.python_type == datetime
        assert not rent_start_column.primary_key
        assert len(rent_start_column.foreign_keys) == 0
        assert not rent_start_column.nullable

        rent_end_column: Column = spaceship_rent_table.columns['rent_end']
        assert rent_end_column.type.python_type == datetime
        assert not rent_end_column.primary_key
        assert len(rent_end_column.foreign_keys) == 0
        assert not rent_end_column.nullable

        MigrationsHelper.rollback(1)


if __name__ == '__main__':
    MigrationsHelper.update(5)
