from logging import getLogger
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from bookmarker.config import get_settings
from bookmarker.db.models import Bookmark, Tag


logger = getLogger(__name__)


class TestDeleteBookmark:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/bookmark"

    @staticmethod
    async def check_bookmark_not_exist(bookmark: Bookmark, session: AsyncSession):
        query = select(Bookmark).filter(Bookmark.id == bookmark.id)
        assert len((await session.scalars(query)).all()) == 0

    @staticmethod
    async def check_tag_exist(tag: Tag, session: AsyncSession):
        query = select(Tag).filter(Tag.id == tag.id)
        assert len((await session.scalars(query)).all()) == 1

    async def test_auth(self, client):
        response = await client.delete(f"{self.get_url()}/{uuid4()}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_existing_bookmark_without_tag(self, client, bookmark_without_tag, user_with_auth_token, session):
        response = await client.delete(
            url=f"{self.get_url()}/{bookmark_without_tag.id}",
            headers=user_with_auth_token["header"],
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        await self.check_bookmark_not_exist(bookmark_without_tag, session)

    async def test_existing_bookmark_with_tag(  # pylint: disable=too-many-arguments
        self, client, bookmark_with_tag, user_with_auth_token, tag, session
    ):
        response = await client.delete(
            url=f"{self.get_url()}/{bookmark_with_tag.id}",
            headers=user_with_auth_token["header"],
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        await self.check_bookmark_not_exist(bookmark_with_tag, session)
        await self.check_tag_exist(tag, session)

    async def test_not_existing_bookmark(self, client, user_with_auth_token):
        response = await client.delete(
            url=f"{self.get_url()}/{uuid4()}",
            headers=user_with_auth_token["header"],
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
