from pytest import fixture

from bookmarker.db.models import Bookmark


@fixture
async def bookmark_without_tag(session, user_with_auth_token):
    bookmark_object = Bookmark(
        title="My bookmark without tag",
        link="https://yandex.net/",
        owner_id=user_with_auth_token["model"].id,
    )
    session.add(bookmark_object)
    await session.commit()
    await session.refresh(bookmark_object)
    return bookmark_object


@fixture
async def bookmark_with_tag(session, user_with_auth_token, tag):
    bookmark_object = Bookmark(
        title="My bookmark with tag",
        link="https://yandex.ru/",
        owner_id=user_with_auth_token["model"].id,
        tag=tag.name,
    )
    session.add(bookmark_object)
    await session.commit()
    await session.refresh(bookmark_object)
    return bookmark_object
