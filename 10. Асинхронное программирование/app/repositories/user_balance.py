from typing import Optional
from sqlalchemy import select

from app.repositories import BaseRepository
from app.db.models import UserBalance as UserBalanceModel


class UserBalance(BaseRepository):
    async def get_by_id(self, user_id: str) -> Optional[UserBalanceModel]:
        query = select(UserBalanceModel).where(
            UserBalanceModel.user_id == user_id
        )
        item = await self.session.scalar(query)
        if not item:
            return None
        return item
