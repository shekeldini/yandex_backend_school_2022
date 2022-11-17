import pytest
from app.services import ServiceRegistry
from app.config import Config


class TestGetAliveServices:
    async def test_alive_services(self, mock_get_service_list):
        links_services = Config().get_service_list()
        print(links_services)
        service_registry = ServiceRegistry(links_services)
        assert len(links_services) == len(service_registry.get_alive_services())

    @pytest.mark.parametrize(
        "links_services",
        [
            ["invalid"],
            ["localhost:1000"],
            ["wrong:1000"]
        ],
    )
    async def test_not_available_service(self, links_services):
        service_registry = ServiceRegistry(links_services)
        assert not service_registry.get_alive_services()
