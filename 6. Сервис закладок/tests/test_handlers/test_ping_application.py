import pytest
from starlette import status

pytestmark = pytest.mark.asyncio


class TestPingApplication:
    @staticmethod
    def get_ping_application_url() -> str:
        return "/api/v1/health_check/ping_application"

    async def test_ping_application(self, client):
        response = await client.get(url=self.get_ping_application_url())
        assert response.status_code == status.HTTP_200_OK
