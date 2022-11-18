import pytest
from starlette import status

pytestmark = pytest.mark.asyncio


class TestPingDatabase:
    @staticmethod
    def get_ping_database_url() -> str:
        return "/api/v1/health_check/ping_database"

    async def test_ping_database(self, client):
        response = await client.get(url=self.get_ping_database_url())
        assert response.status_code == status.HTTP_200_OK
