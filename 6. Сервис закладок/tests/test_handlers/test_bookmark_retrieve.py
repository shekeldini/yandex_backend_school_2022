import pytest
from starlette import status

from tests.utils import create_item

pytestmark = pytest.mark.asyncio


class TestBookmarkRetrieve:
    @staticmethod
    def get_url(sort_key, tag=None) -> str:
        if tag:
            return f"/api/v1/bookmark?sort_key={sort_key}&page=1&size=50&tag={tag}"
        return "/api/v1/bookmark?sort_key=BY_ID&page=1&size=50"

    async def test_invalid_access_token(self, client):
        response = await client.get(
            url=self.get_url(sort_key="BY_ID", tag="test"),
            headers={
                "Authorization": "Bearer ",
                "accept": "application / json"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "sort_key",
        (
            "BY_ID",
            "BY_DATE",
            "BY_TITLE",
            "BY_LINK",
        ),
    )
    async def test_with_tag(self, client, user_data_sample, sort_key):
        _, access_token = await create_item(client, user_data_sample, "test")
        await create_item(client, user_data_sample, "test")
        await create_item(client, user_data_sample, "test1")
        response = await client.get(
            url=self.get_url(sort_key=sort_key, tag="test"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "accept": "application / json"
            }
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert len(response_data["items"]) == 2

    async def test_main_scenario(self, client, user_data_sample):
        _, access_token = await create_item(client, user_data_sample, "test")
        await create_item(client, user_data_sample, "test")
        await create_item(client, user_data_sample, "test1")
        response = await client.get(
            url=self.get_url("BY_ID"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "accept": "application / json"
            }
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert len(response_data["items"]) == 3
