from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status

from shortener import utils
from shortener.db.connection import get_db
from shortener.db.models import UrlStorage


api_router = APIRouter(tags=["Url"])


@api_router.get(
    "/{short_code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={status.HTTP_404_NOT_FOUND: {"description": "URL `request.url` doesn't exist"}},
)
async def get_long_url(
    request: Request,
    short_code: str = Path(...),
    id_: Optional[UUID] = Query(default=None, alias="id"),
    db: Session = Depends(get_db),
):
    """
    Логика работы ручки:

    Проверяем, что у нас есть short_code в базе:
      - если он уже есть, то совершаем редирект на длинный урл + увеличиваем счетчик переходов на 1
      - если нет, то кидаем ошибку;
    """
    db_url: UrlStorage = (
        db.query(UrlStorage)
        .where(
            and_(
                UrlStorage.short_url == short_code,
                UrlStorage.dt_expired >= utils.get_now_date()
            )
        )
        .first()
    )
    if db_url:
        if not id_:
            db_url.number_of_clicks += 1
            db.commit()
        elif db_url == id_:
            db_url.number_of_use_qr_code += 1
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid id")
        return RedirectResponse(db_url.long_url)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"URL '{request.url}' doesn't exist")
