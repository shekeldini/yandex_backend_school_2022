from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from bookmarker.config import get_settings
from bookmarker.db.models import Bookmark, User


class TestTakeOut:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/user/takeout"

    @staticmethod
    async def check_bookmark_not_exist(bookmark: Bookmark, session: AsyncSession):
        query = select(Bookmark).filter(Bookmark.id == bookmark.id)
        assert len((await session.scalars(query)).all()) == 0

    async def test_not_authenticated(self, client):
        response = await client.delete(url=self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_authenticated(self, client, user_with_auth_token, session):
        response = await client.delete(url=self.get_url(), headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Проверяем, что пользователь реально исчезает из базы
        query = select(User).filter(User.username == user_with_auth_token["model"].username)
        users_in_base = (await session.scalars(query)).all()
        assert len(users_in_base) == 0

        # Проверяем, что уже не может дернуть ручку, потому что не пройдет авторизация
        response = await client.delete(url=self.get_url(), headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_user_with_bookmark(self, client, user_with_auth_token, bookmark_with_tag, session):
        response = await client.delete(url=self.get_url(), headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_204_NO_CONTENT
        await self.check_bookmark_not_exist(bookmark_with_tag, session)
