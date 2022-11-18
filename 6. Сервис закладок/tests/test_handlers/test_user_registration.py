import pytest
from starlette import status

pytestmark = pytest.mark.asyncio


class TestUserRegistration:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/user/registration"

    async def test_invalid_email(self, client):
        data = {
            "username": "user_name1",
            "password": "password123",
            "email": "some-bad-url"
        }
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_main_scenario(self, client):
        data = {
            "username": "valid_user_name",
            "password": "valid_password",
            "email": "valid@yandex.ru"
        }
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_201_CREATED

    async def test_duplicate(self, client, user_data_sample):
        data = {
            "username": user_data_sample.username,
            "password": user_data_sample.password,
            "email": user_data_sample.email
        }
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Username already exists."
