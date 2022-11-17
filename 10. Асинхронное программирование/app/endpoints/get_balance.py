import json
from datetime import datetime
from fastapi import APIRouter, Depends, Path, Query, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
from app.models.response import GetBalance
from app.repositories import ChangesHistory
from app.services import logger
from app.utils import create_base_log

api_router = APIRouter(tags=["Url"])


@api_router.get(
    "/{userId}/balance/",
    response_model=GetBalance
)
async def get_balance(
        request: Request,
        user_id: str = Path(alias="userId"),
        timestamp: datetime = Query(...),
        session: AsyncSession = Depends(get_session)
):
    base_log = await create_base_log(request)

    balance = await ChangesHistory(session).get_balance(
        user_id,
        timestamp.replace(tzinfo=None)
    )
    if not balance:
        await logger.info(json.dumps({**base_log, "status_code": status.HTTP_404_NOT_FOUND}))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found"
        )
    await logger.info(json.dumps({**base_log, "status_code": status.HTTP_200_OK}))
    return GetBalance(balance=balance)
