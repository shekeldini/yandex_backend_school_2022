from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Request, Response
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from bookmarker.db.connection import get_session
from bookmarker.db.enums import BookmarksSortKey
from bookmarker.db.models import User
from bookmarker.schemas import Bookmark as BookmarkSchema
from bookmarker.schemas import BookmarkCreateRequest
from bookmarker.utils import bookmark as utils
from bookmarker.utils.user import get_current_user


api_router = APIRouter(
    prefix="/bookmark",
    tags=["Bookmark"],
)


@api_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=BookmarkSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def create(
    _: Request,
    bookmark_instance: BookmarkCreateRequest = Body(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    title = utils.get_page_title(bookmark_instance.link)
    return await utils.create_bookmark(session, current_user, bookmark_instance, title)


@api_router.get(
    "/{bookmark_id}",
    status_code=status.HTTP_200_OK,
    response_model=BookmarkSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Bookmark with this id and this owner not found",
        },
    },
)
async def retrieve(
    _: Request,
    bookmark_id: UUID4 = Path(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    bookmark = await utils.get_bookmark(session, current_user, bookmark_id)
    if bookmark:
        return BookmarkSchema.from_orm(bookmark)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Bookmark with this id and this owner not found",
    )


@api_router.delete(
    "/{bookmark_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def delete(
    _: Request,
    bookmark_id: UUID4 = Path(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await utils.delete_bookmark(session, current_user, bookmark_id)


@api_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=Page[BookmarkSchema],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
    },
)
async def retrieve_list(
    _: Request,
    current_user: User = Depends(get_current_user),
    tag_filter: list[str] = Query(default=[], alias="tag"),
    sort_key: BookmarksSortKey = Query(default=BookmarksSortKey.BY_ID),
    session: AsyncSession = Depends(get_session),
):
    query = utils.build_query_for_retrieve_list_of_bookmarks(current_user, tag_filter, sort_key)
    return await paginate(session, query)
