import pytest
from sqlalchemy import MetaData

from MigrationsHelper import MigrationsHelper
import sqlalchemy as alchemy


@pytest.fixture(autouse=True)
def run_around_tests():
    meta_data = MetaData(bind=MigrationsHelper.db)
    alchemy.MetaData.reflect(meta_data)
    meta_data.drop_all()
    yield
    meta_data.drop_all()