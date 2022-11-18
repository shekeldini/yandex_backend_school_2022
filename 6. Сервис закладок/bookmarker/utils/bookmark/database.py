from pydantic import UUID4
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as future_select
from sqlalchemy.orm import joinedload

from bookmarker.db.enums import BookmarksSortKey
from bookmarker.db.models import Bookmark, Tag, User
from bookmarker.schemas import Bookmark as BookmarkSchema
from bookmarker.schemas import BookmarkCreateRequest


async def create_bookmark(
    session: AsyncSession,
    owner: User,
    bookmark_schema: BookmarkCreateRequest,
    parsed_title: str,
) -> BookmarkSchema:
    new_bookmark = Bookmark(
        title=parsed_title,
        link=bookmark_schema.link,
        owner_id=owner.id,
    )
    if bookmark_schema.tag is not None:
        search_tag_query = select(Tag).where(Tag.name == bookmark_schema.tag)
        tag = await session.scalar(search_tag_query)
        if tag is None:
            tag = Tag(name=bookmark_schema.tag)
            session.add(tag)
            await session.commit()

        new_bookmark.tag = tag.name

    session.add(new_bookmark)
    await session.commit()
    await session.refresh(new_bookmark)

    return BookmarkSchema.from_orm(new_bookmark)


async def get_bookmark(
    session: AsyncSession,
    owner: User,
    bookmark_id: UUID4,
) -> BookmarkSchema | None:
    get_bookmark_query = select(Bookmark).where(
        and_(
            Bookmark.owner_id == owner.id,
            Bookmark.id == bookmark_id,
        )
    )
    bookmark_from_base = await session.scalar(get_bookmark_query)
    if bookmark_from_base is None:
        return None
    return BookmarkSchema.from_orm(bookmark_from_base)


async def delete_bookmark(
    session: AsyncSession,
    owner: User,
    bookmark_id: UUID4,
) -> None:
    delete_bookmark_query = delete(Bookmark).where(
        and_(
            Bookmark.owner_id == owner.id,
            Bookmark.id == bookmark_id,
        )
    )
    await session.execute(delete_bookmark_query)
    await session.commit()


def build_query_for_retrieve_list_of_bookmarks(
    current_user: User,
    tag_filter: list[str],
    sort_key: BookmarksSortKey | None,
) -> select:
    query = select(Bookmark).filter(Bookmark.owner_id == current_user.id)
    if tag_filter:
        query = query.filter(Bookmark.tag.in_(tag_filter))

    match sort_key:
        case BookmarksSortKey.BY_ID:
            query = query.order_by(Bookmark.id)
        case BookmarksSortKey.BY_DATE:
            query = query.order_by(Bookmark.dt_created)
        case BookmarksSortKey.BY_LINK:
            query = query.order_by(Bookmark.link)
        case BookmarksSortKey.BY_TITLE:
            query = query.order_by(Bookmark.title)
        case _:
            query = query.order_by(Bookmark.id)
    return query
