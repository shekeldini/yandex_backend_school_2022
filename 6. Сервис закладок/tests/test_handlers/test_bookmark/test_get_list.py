import pytest
from starlette import status

from bookmarker.config import get_settings
from bookmarker.db.enums import BookmarksSortKey


class TestGetBookmarkList:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/bookmark"

    async def test_auth(self, client):
        response = await client.get(self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_empty_list(self, client, user_with_auth_token):
        response = await client.get(
            url=self.get_url(),
            headers=user_with_auth_token["header"],
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["items"] == []

    async def test_without_filters(self, client, user_with_auth_token, bookmark_with_tag):  # pylint: disable=W0613
        response = await client.get(
            url=self.get_url(),
            headers=user_with_auth_token["header"],
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["items"]) == 1

    async def test_filter_by_tag(
        self, client, user_with_auth_token, bookmark_with_tag, bookmark_without_tag  # pylint: disable=W0613
    ):
        response = await client.get(
            url=self.get_url(),
            headers=user_with_auth_token["header"],
            params={
                "tag": bookmark_with_tag.tag,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["items"]) == 1

    @pytest.mark.parametrize(
        "sort_key",
        (
            BookmarksSortKey.BY_ID,
            BookmarksSortKey.BY_LINK,
            BookmarksSortKey.BY_DATE,
            BookmarksSortKey.BY_TITLE,
        ),
    )
    async def test_with_sort_keys(  # pylint: disable=too-many-arguments
        self, client, user_with_auth_token, bookmark_with_tag, bookmark_without_tag, sort_key
    ):
        response = await client.get(
            url=self.get_url(),
            headers=user_with_auth_token["header"],
            params={
                "sort_key": sort_key.value,
            },
        )
        assert response.status_code == status.HTTP_200_OK

        bookmarks = [bookmark_without_tag, bookmark_with_tag]
        match sort_key:
            case BookmarksSortKey.BY_ID:
                key, reverse = "id", False
            case BookmarksSortKey.BY_LINK:
                key, reverse = "link", False
            case BookmarksSortKey.BY_DATE:
                key, reverse = "dt_created", False
            case BookmarksSortKey.BY_TITLE:
                key, reverse = "title", True
            case _:
                key, reverse = "id", False
        response_data_ids = list(map(lambda x: x["id"], response.json()["items"]))
        sorted_bookmark_ids = list(
            map(lambda x: str(x.id), sorted(bookmarks, key=lambda x: getattr(x, key), reverse=reverse))
        )
        assert response_data_ids == sorted_bookmark_ids
