import pytest
from starlette import status

pytestmark = pytest.mark.asyncio


class TestUserAuthentication:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/user/authentication"

    async def test_not_found(self, client):
        data = {
            "username": "test_user",
            "password": "test_pwd"
        }
        response = await client.post(url=self.get_url(), data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Incorrect username or password"

    async def test_main_scenario(self, client, user_data_sample):
        data = {
            "username": user_data_sample.username,
            "password": "test",
        }
        response = await client.post(
            url=self.get_url(),
            data=data,
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "accept": "application / json"
            }
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

    async def test_wrong_password(self, client, user_data_sample):
        data = {
            "username": user_data_sample.username,
            "password": "test_test",
        }
        response = await client.post(
            url=self.get_url(),
            data=data,
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "accept": "application / json"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
