from typing import Union, List

from fastapi import APIRouter, Query, Depends

from sqlalchemy.orm import Session
from starlette import status as response_status

from app.db.connection import get_db
from app.schemas import Status
from app.schemas.response import ProblemItem
from app.utils import get_user, can_buy
api_router = APIRouter(tags=["Url"])


@api_router.get(
    "/check",
    response_model=List[ProblemItem],
    status_code=response_status.HTTP_200_OK
)
async def check(
    user_id: int = Query(...),
    item_id_list: Union[list[str], None] = Query(default=None, alias="item_id"),
    db: Session = Depends(get_db)
):
    result = []
    user_repository, user = await get_user(user_id, db)
    for item_id in item_id_list:
        status = await can_buy(
            item_id=item_id,
            user_repository=user_repository,
            user=user,
            db=db
        )
        if status != Status.OK:
            result.append(ProblemItem(item_id=item_id, problem=status.value))
    return result
