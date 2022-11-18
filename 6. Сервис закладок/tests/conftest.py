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
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from tests.utils import make_alembic_config

from bookmarker.__main__ import get_app
from bookmarker.db.connection import SessionManager
from bookmarker.db.models import User
from bookmarker.config.utils import get_settings


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
    settings.POSTGRES_DB = tmp_name
    environ["POSTGRES_DB"] = tmp_name

    tmp_url = settings.database_uri_sync
    if not database_exists(settings.database_uri_sync):
        create_database(settings.database_uri_sync)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(config="bookmarker/db/", name="alembic", pg_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture
def migrated_postgres(alembic_config: Config):
    """
    Проводит миграции.
    """
    upgrade(alembic_config, "head")


@pytest.fixture
async def client(migrated_postgres, manager: SessionManager = SessionManager()) -> Session:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_app()
    manager.refresh_sinc()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    yield AsyncClient(app=app, base_url="http://test")


@pytest.fixture
async def database(postgres, migrated_postgres, manager: SessionManager = SessionManager()) -> Session:
    """
    Returns a class object with which you can create a new session to connect to the database.
    """
    manager.refresh_sinc()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    database = manager.get_sinc_session()
    try:
        yield database
    finally:
        database.close()


@pytest.fixture
async def user_data_sample(database) -> User:
    """
    Create user sample for tests.
    """
    settings = get_settings()
    new_object = User(
        username="test",
        password=settings.PWD_CONTEXT.hash("test"),
        email="test@yandex.ru"
    )
    database.add(new_object)
    database.commit()
    database.refresh(new_object)
    return new_object
