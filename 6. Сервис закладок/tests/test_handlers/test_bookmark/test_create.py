from logging import getLogger

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from bookmarker.config import get_settings
from bookmarker.db.models import Bookmark, User


logger = getLogger(__name__)


class TestCreateBookmark:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/bookmark"

    @staticmethod
    async def check_bookmark_in_base(user: User, link: str, session: AsyncSession):
        """
        Проверяем, что действительно создалась закладка, принадлежащая этому пользователю
        """
        query = select(Bookmark).filter(
            and_(
                Bookmark.link == link,
                Bookmark.owner_id == user.id,
                Bookmark.title == "My beautiful bookmark",
            )
        )
        assert len((await session.scalars(query)).all()) == 1

    async def test_auth(self, client):
        response = await client.post(self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_without_tag(self, client, user_with_auth_token, session):
        data = {
            "link": "https://my_personal_web_site.me/",
        }
        response = await client.post(self.get_url(), json=data, headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_201_CREATED
        await self.check_bookmark_in_base(user_with_auth_token["model"], data["link"], session)

    async def test_create_with_new_tag(self, client, user_with_auth_token, session):
        data = {
            "link": "https://my_personal_web_site.me/",
            "tag": "My new tag",
        }
        response = await client.post(self.get_url(), json=data, headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_201_CREATED
        await self.check_bookmark_in_base(user_with_auth_token["model"], data["link"], session)

    async def test_create_with_existing_tag(self, client, user_with_auth_token, session, tag):
        data = {
            "link": "https://my_personal_web_site.me/",
            "tag": tag.name,
        }
        response = await client.post(self.get_url(), json=data, headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_201_CREATED
        await self.check_bookmark_in_base(user_with_auth_token["model"], data["link"], session)
