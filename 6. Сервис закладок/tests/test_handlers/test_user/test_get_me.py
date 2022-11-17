from starlette import status

from bookmarker.config import get_settings


class TestGetMe:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/user/me"

    async def test_with_header(self, client, user_with_auth_token):
        response = await client.get(url=self.get_url(), headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_200_OK
        response_body = response.json()
        assert response_body["username"] == user_with_auth_token["model"].username

    async def test_without_header(self, client, user_with_auth_token):  # pylint: disable=unused-argument
        response = await client.get(url=self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
