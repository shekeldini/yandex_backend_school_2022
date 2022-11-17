from app.main import startup
from app.services import statistic
from tests.utils import get_available_services


class TestStartUp:
    async def test_startup(self, mock_get_alive_services):
        startup()
        assert len(statistic.get_services_list()) == len(get_available_services())
