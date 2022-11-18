import pytest
from starlette import status

from tests.utils import create_item, invalid_access_token_get

pytestmark = pytest.mark.asyncio


class TestBookmarkGet:
    @staticmethod
    def get_url(bookmark_id) -> str:
        return f"/api/v1/bookmark/{bookmark_id}"

    async def test_main_scenario(self, client, user_data_sample):
        response_data, token = await create_item(client, user_data_sample, "test")
        response = await client.get(
            url=self.get_url(response_data["id"]),
            headers={
                "Authorization": f"Bearer {token}",
                "accept": "application / json"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == response_data["id"]

    async def test_invalid_access_token(self, client, user_data_sample):
        response_data, _ = await create_item(client, user_data_sample, "test")
        response = await invalid_access_token_get(client, self.get_url(response_data["id"]))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
