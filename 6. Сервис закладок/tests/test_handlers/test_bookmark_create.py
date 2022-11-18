import pytest
from starlette import status

from tests.utils import auth_user

pytestmark = pytest.mark.asyncio


class TestBookmarkCreate:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/bookmark"

    async def test_invalid_access_token(self, client):
        data = {
            "link": "https://vk.com/",
            "tag": "test"
        }
        response = await client.post(
            url=self.get_url(),
            json=data,
            headers={"Authorization": "Bearer ", "accept": "application / json"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_invalid_link(self, client, user_data_sample):
        response_data = await auth_user(client, user_data_sample)
        data = {
            "link": "bad-link",
            "tag": "test"
        }
        response = await client.post(
            url=self.get_url(),
            json=data,
            headers={
                "Authorization": f"Bearer {response_data['access_token']}",
                "accept": "application / json"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_main_scenario(self, client, user_data_sample):
        response_data = await auth_user(client, user_data_sample)
        data = {
            "link": "https://vk.com/",
            "tag": "test"
        }
        response = await client.post(
            url=self.get_url(),
            json=data,
            headers={
                "Authorization": f"Bearer {response_data['access_token']}",
                "accept": "application / json"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
