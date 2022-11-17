from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.exceptions import TooMuchRetry
from app.models.others import CreateToken
from app.endpoints.depends import get_context
router = APIRouter()


@router.get("/token", response_model=str)
async def import_digital_items(
        id_: Optional[str] = Query(default=None, alias="id"),
        timestamp: Optional[int] = Query(default=None),
        context=Depends(get_context)
):
    model = CreateToken(
        id=id_,
        timestamp=timestamp
    )
    status_code, response_data = await context.create_token(model)
    if status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
        raise TooMuchRetry(
            status_code=status_code,
            detail=response_data
        )
    return response_data
