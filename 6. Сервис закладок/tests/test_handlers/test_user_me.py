import pytest
from starlette import status

from tests.utils import auth_user

pytestmark = pytest.mark.asyncio


class TestUserMe:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/user/me"

    async def test_main_scenario(self, client, user_data_sample):
        response_data = await auth_user(client, user_data_sample)

        response = await client.get(
            url=self.get_url(),
            headers={
                "Authorization": f"Bearer {response_data['access_token']}",
                "accept": "application / json"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == user_data_sample.username

    async def test_invalid_access_token(self, client):
        response = await client.get(
            url=self.get_url(),
            headers={
                "Authorization": "Bearer ",
                "accept": "application / json"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
