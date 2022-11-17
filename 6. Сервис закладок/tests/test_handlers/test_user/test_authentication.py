from starlette import status

from tests.utils import UserFactory, generate_strong_password

from bookmarker.config import get_settings


class TestAuthentication:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/user/authentication"

    async def test_success_authentication(self, client, user_with_auth_token):
        data = {
            "username": user_with_auth_token["model"].username,
            "password": user_with_auth_token["password"],
        }
        response = await client.post(url=self.get_url(), data=data)
        assert response.status_code == status.HTTP_200_OK

    async def test_user_not_found(self, client):
        user = UserFactory()
        data = {
            "username": user.username,
            "password": user.password,
        }
        response = await client.post(url=self.get_url(), data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_incorrect_password(self, client, user_with_auth_token):
        data = {
            "username": user_with_auth_token["model"].username,
            "password": generate_strong_password(),
        }
        response = await client.post(url=self.get_url(), data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
