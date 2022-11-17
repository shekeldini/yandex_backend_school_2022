from fastapi import APIRouter, Depends, Path
from fastapi.responses import Response
from pydantic import UUID4
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette import status

from shortener.db.connection import get_db
from shortener.db.models import UrlStorage


api_router = APIRouter(tags=["Url"])


@api_router.delete(
    "/admin/{secret_key}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_link(
    secret_key: UUID4 = Path(...),
    db: Session = Depends(get_db),
):
    query = delete(UrlStorage).where(UrlStorage.secret_key == secret_key)
    db.execute(query)
    db.commit()
