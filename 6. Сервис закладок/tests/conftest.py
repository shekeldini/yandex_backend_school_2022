# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from asyncio import get_event_loop_policy
from os import environ
from types import SimpleNamespace
from uuid import uuid4

import pytest
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient
from mock import Mock
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from tests.utils import make_alembic_config

from bookmarker.__main__ import get_app
from bookmarker.config import get_settings
from bookmarker.db.connection import SessionManager
from bookmarker.utils import bookmark as utils


pytest_plugins = [
    "fixtures.user",
    "fixtures.bookmark",
    "fixtures.tag",
]


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
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
    if not database_exists(tmp_url):
        create_database(tmp_url)

    try:
        yield settings.database_uri
    finally:
        drop_database(tmp_url)


def run_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    upgrade(cfg, "head")


async def run_async_upgrade(config: Config, database_uri: str):
    async_engine = create_async_engine(database_uri, echo=True)
    async with async_engine.begin() as conn:
        await conn.run_sync(run_upgrade, config)


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(config="bookmarker/db/", name="alembic", pg_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture
def alembic_engine():
    """
    Override this fixture to provide pytest-alembic powered tests with a database handle.
    """
    settings = get_settings()
    return create_async_engine(settings.database_uri_sync, echo=True)


@pytest.fixture
async def migrated_postgres(postgres, alembic_config: Config):
    """
    Проводит миграции.
    """
    await run_async_upgrade(alembic_config, postgres)


@pytest.fixture
async def client(migrated_postgres, manager: SessionManager = SessionManager()) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_app()
    utils.get_page_title = Mock(return_value="My beautiful bookmark")
    manager.refresh()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    yield AsyncClient(app=app, base_url="http://test")


@pytest.fixture
async def engine_async(postgres) -> AsyncEngine:
    engine = create_async_engine(postgres, future=True)
    yield engine
    await engine.dispose()


@pytest.fixture
def session_factory_async(engine_async) -> sessionmaker:
    return sessionmaker(engine_async, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def session(session_factory_async) -> AsyncSession:
    async with session_factory_async() as session:
        yield session


@pytest.fixture
def set_wrong_port_for_postgres():  # нужна для единственного теста - проверки ping при сломанной базе
    settings = get_settings()
    old_port = settings.POSTGRES_PORT
    environ["POSTGRES_PORT"] = str(old_port + 1)
    manager = SessionManager()
    manager.refresh()
    yield
    environ["POSTGRES_PORT"] = str(old_port)
