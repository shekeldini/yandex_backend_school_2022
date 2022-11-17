# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from asyncio import new_event_loop, set_event_loop
from os import environ
from types import SimpleNamespace
from uuid import uuid4

import pytest
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient
from mock import AsyncMock
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from tests.utils import make_alembic_config

import shortener.utils as utils_module
from shortener.__main__ import get_app
from shortener.db.connection import SessionManager
from shortener.db.models import UrlStorage
from shortener.utils import get_settings


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    loop = new_event_loop()
    set_event_loop(loop)

    yield loop
    loop.close()


@pytest.fixture()
def postgres() -> str:
    """
    Создает временную БД для запуска теста.
    """
    settings = get_settings()

    tmp_name = ".".join([uuid4().hex, "pytest"])
    settings.DB_NAME = tmp_name
    environ["DB_NAME"] = tmp_name

    tmp_url = settings.database_uri
    if not database_exists(settings.database_uri):
        create_database(settings.database_uri)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(config="shortener/db/", name="alembic", pg_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture
def migrated_postgres(alembic_config: Config):
    """
    Проводит миграции.
    """
    upgrade(alembic_config, "head")


@pytest.fixture
async def client(migrated_postgres, manager: SessionManager = SessionManager()) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_app()
    manager.refresh()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    utils_module.check_website_exist = AsyncMock(return_value=(True, "Status code < 400"))
    yield AsyncClient(app=app, base_url="http://test")


@pytest.fixture
async def database(postgres, migrated_postgres, manager: SessionManager = SessionManager()) -> Session:
    """
    Returns a class object with which you can create a new session to connect to the database.
    """
    manager.refresh()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    database = manager.get_session()
    try:
        yield database
    finally:
        database.close()


@pytest.fixture
async def data_sample(database) -> UrlStorage:
    """
    Creates minimum data sample for tests.
    """
    suffix = str(uuid4())[:5]
    new_object = UrlStorage(
        long_url=f"https://{uuid4()}.com",
        short_url=suffix,
    )
    database.add(new_object)
    database.commit()
    database.refresh(new_object)
    return new_object
