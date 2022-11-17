import pytest
from starlette import status


pytestmark = pytest.mark.asyncio


class TestHealthCheckHandler:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/health_check/ping"

    async def test_ping(self, client):
        response = await client.get(url=self.get_url())
        assert response.status_code == status.HTTP_200_OK
