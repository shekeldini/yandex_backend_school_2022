import io
from qrcode import make

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import StreamingResponse

from shortener import utils
from shortener.db.connection import get_db
from shortener.db.models import UrlStorage
from shortener.schemas import QRRequest

api_router = APIRouter(tags=["QR"])


@api_router.post(
    "/qr",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse
)
async def make_qr(
    model: QRRequest = Body(
        ..., example={
            "secret_key": "1439bb6f-e9fc-4be9-890e-e2146b3f6086"
        }
    ),
    db: Session = Depends(get_db)
):
    """
    Идем в базу, ищем запись где UrlStorage.secret_key = QRRequest.secret_key и UrlStorage.dt_expired >= current_time.
      - Если такой записи отдаем пользователю HTTP_404_NOT_FOUND.
      - Если такая запись существует.
        - Отдаем пользователю сгенерированный QR код в котором содержится url вида
         {host}:{port}{prefix}/{suffix}?id={UrlStorage.id}
    """
    db_url: UrlStorage = (
        db.query(UrlStorage).where(
            and_(
                UrlStorage.secret_key == model.secret_key,
                UrlStorage.dt_expired >= utils.get_now_date()
            )
        ).first()
    )
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link with this secret key is not found."
        )
    url = f"{utils.url_from_suffix(db_url.short_url)}?id={db_url.id}"
    img = make(url)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/jpeg")
