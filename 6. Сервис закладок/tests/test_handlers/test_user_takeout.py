import pytest
from starlette import status

from tests.utils import auth_user, invalid_access_token_delete

pytestmark = pytest.mark.asyncio


class TestUserTakeout:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/user/takeout"

    async def test_invalid_access_token(self, client):
        response = await invalid_access_token_delete(client, self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_main_scenario(self, client, user_data_sample):
        response_data = await auth_user(client, user_data_sample)

        response = await client.delete(
            url=self.get_url(),
            headers={
                "Authorization": f"Bearer {response_data['access_token']}",
                "accept": "application / json"
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = await client.delete(
            url=self.get_url(),
            headers={
                "Authorization": f"Bearer {response_data['access_token']}",
                "accept": "application / json"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
