# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import asyncio
import pytest
from asyncio import get_event_loop_policy
from httpx import AsyncClient
from app.main import get_app
from app.models.others import CreateToken
from app.services import statistic, ServiceRegistry
from app.utils import get_settings
from app.config import Config
from app.services.strategies import RoundRobin
from tests.utils import get_service_response, get_available_services
from mock import Mock, patch


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mock_create_request():
    """
    Mock get_data from RoundRobin
    """
    future = asyncio.Future()
    future.set_result(get_service_response())
    RoundRobin.create_request = Mock(
        return_value=future
    )


@pytest.fixture
async def mock_service_statistic():
    future = asyncio.Future()
    future.set_result(None)
    statistic.write_statistic = Mock(
        return_value=future
    )


@pytest.fixture
async def mock_create_token():
    future = asyncio.Future()
    future.set_result((503, "Service Unavailable"))
    RoundRobin.create_token = Mock(
        return_value=future
    )


@pytest.fixture
def service_statistic(mock_service_statistic):
    for i in get_available_services():
        statistic.set_service(i)
    return statistic


@pytest.fixture
async def mock_get_alive_services():
    ServiceRegistry.get_alive_services = Mock(
        return_value=get_available_services()
    )


@pytest.fixture
async def mock_get_service_list(service_statistic):
    """
    Mock get_service_list
    """
    get_settings.get_service_list = Mock(
        return_value=get_available_services()
    )
    Config.get_service_list = Mock(
        return_value=get_available_services()
    )


@pytest.fixture
async def client(mock_get_service_list) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_app()
    yield AsyncClient(app=app, base_url="http://test")


@pytest.fixture
def token() -> CreateToken:
    return CreateToken(
        id="test",
        timestamp=0
    )
