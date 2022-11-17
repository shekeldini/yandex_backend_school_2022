from uuid import uuid4

from starlette import status

from bookmarker.config import get_settings


class TestGetBookmark:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/bookmark"

    async def test_auth(self, client):
        response = await client.get(f"{self.get_url()}/{uuid4()}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_existing_bookmark(self, client, bookmark_without_tag, user_with_auth_token):
        response = await client.get(
            url=f"{self.get_url()}/{bookmark_without_tag.id}",
            headers=user_with_auth_token["header"],
        )
        assert response.status_code == status.HTTP_200_OK

    async def test_not_existing_bookmark(self, client, user_with_auth_token):
        response = await client.get(
            url=f"{self.get_url()}/{uuid4()}",
            headers=user_with_auth_token["header"],
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
