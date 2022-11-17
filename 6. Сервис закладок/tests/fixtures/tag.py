from pytest import fixture

from bookmarker.db.models import Tag


@fixture
async def tag(session) -> Tag:
    tag_object = Tag(name="New tag")
    session.add(tag_object)
    await session.commit()
    await session.refresh(tag_object)
    return tag_object
