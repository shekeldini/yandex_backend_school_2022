import datetime
from random import choice
from string import ascii_uppercase, digits

from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette import status

from shortener import utils
from shortener.db.connection import get_db
from shortener.db.models import UrlStorage
from shortener.schemas import MakeShorterRequest, MakeShorterResponse, TimeUnit


api_router = APIRouter(tags=["Url"])


async def get_short(db: Session) -> tuple[str, str]:
    while True:
        suffix = "".join(choice(ascii_uppercase + digits) for _ in range(5))
        exist = await suffix_exist(db, suffix)
        if not exist:
            break
    short_url = utils.url_from_suffix(suffix)
    return short_url, suffix


async def suffix_exist(db: Session, suffix: str) -> bool:
    exist: UrlStorage = db.query(UrlStorage).where(UrlStorage.short_url == suffix).first()
    if exist and exist.dt_expired < utils.get_now_date():
        db.execute(delete(UrlStorage).where(UrlStorage.short_url == suffix))
        db.commit()
        return False
    return bool(exist)


def get_interval(time_to_live: int, time_to_live_unit: TimeUnit) -> datetime.timedelta:
    if time_to_live_unit == TimeUnit.DAYS:
        delta = datetime.timedelta(days=time_to_live)
    elif time_to_live_unit == TimeUnit.HOURS:
        delta = datetime.timedelta(hours=time_to_live)
    elif time_to_live_unit == TimeUnit.MINUTES:
        delta = datetime.timedelta(minutes=time_to_live)
    else:
        delta = datetime.timedelta(seconds=time_to_live)
    return delta


async def create_item(url: str, suffix: str, time_to_live: int, time_to_live_unit: TimeUnit) -> UrlStorage:
    time = utils.get_now_date() + get_interval(time_to_live, time_to_live_unit)
    item = UrlStorage(long_url=str(url), short_url=suffix, dt_expired=time)
    return item


async def valid_site(url: str):
    valid, message = await utils.check_website_exist(url)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    return True


async def create(db: Session, item: UrlStorage):
    db.add(item)
    db.commit()
    db.refresh(item)
    item.short_url = utils.url_from_suffix(item.short_url)
    return MakeShorterResponse.from_orm(item)


@api_router.post(
    "/make_shorter",
    response_model=MakeShorterResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Site with this url does not exists or status code of request >= 400",
        },
    },
)
async def make_shorter(
    model: MakeShorterRequest = Body(
        ..., example={
            "url": "https://yandex.ru",
            "vip_key": "string",
            "time_to_live": 10,
            "time_to_live_unit": "HOURS"
        }
    ),
    db: Session = Depends(get_db),
):
    """
    Логика работы ручки:

    Проверяем, что у нас еще нет сокращенного варианта урла для переданного длинного адреса
      - если он уже есть, то возвращаем его
      - если еще нет:
          1) Подбираем маленький суффикс, которого еще нет в базе;
          2) Сохраняем этот суффикс в базу;
          3) На основе этого суффикса и текущих настроек приложения генерируем полноценный урл;
          4) Возвращаем результат работы ручки: урл и secret_key для запроса дополнительной информации.
    """
    if model.vip_key:
        if await suffix_exist(db, model.vip_key):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Key already exists",
            )
        if await valid_site(model.url):
            item = await create_item(
                model.url,
                model.vip_key,
                model.time_to_live,
                model.time_to_live_unit
            )
            return await create(db=db, item=item)
    else:
        db_url: UrlStorage = db.query(UrlStorage).where(UrlStorage.long_url == model.url).first()
        exist = db_url is not None
        if exist:
            db_url.short_url = utils.url_from_suffix(db_url.short_url)
            return MakeShorterResponse.from_orm(db_url)
        if await valid_site(model.url):
            _, suffix = await get_short(db)
            item = await create_item(
                model.url,
                suffix,
                model.time_to_live,
                model.time_to_live_unit
            )
            return await create(db=db, item=item)
