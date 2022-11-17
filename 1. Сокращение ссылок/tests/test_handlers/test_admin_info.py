from uuid import uuid4

import pytest
from starlette import status


pytestmark = pytest.mark.asyncio


class TestAdminInfoHandler:
    @staticmethod
    def get_url(short_code: str) -> str:
        return f"/api/v1/admin/{short_code}"

    async def test_not_found(self, client):
        short_url = str(uuid4())
        response = await client.get(url=self.get_url(short_url))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_main_scenario(self, client, data_sample, database):
        response = await client.get(url=self.get_url(data_sample.secret_key))
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get("short_url") is not None
        assert response_data.get("long_url") == data_sample.long_url
        assert response_data.get("number_of_clicks") == 0
        assert response_data.get("dt_created") is not None
