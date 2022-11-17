import json

from fastapi import APIRouter, Response, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.models.requests import ChangeBalance
from app.services import can_change, logger
from app.services import change_balance
from app.utils import create_base_log

api_router = APIRouter(tags=["Url"])


@api_router.post(
    "/changeBalance",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Operation rejected",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "SERVER_ERROR",
        },
    }
)
async def route_change_balance(
        request: Request,
        model: ChangeBalance,
        session: AsyncSession = Depends(get_session)
):
    base_log = await create_base_log(request, data=True)
    can = await can_change(**model.dict(), session=session)
    if not can:
        await logger.info(
            json.dumps({
                **base_log,
                "status_code": status.HTTP_403_FORBIDDEN,
                "message": "Can't change balance"
            })
        )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation rejected")
    changed = await change_balance(model, session)
    if not changed:
        await logger.warn(
            json.dumps({
                **base_log,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "SERVER_ERROR"
            })
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SERVER_ERROR")

    await logger.info(
        json.dumps({
            **base_log,
            "status_code": status.HTTP_200_OK,
        })
    )
