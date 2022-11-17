from datetime import datetime
from typing import Optional
from sqlalchemy import select, and_, desc
from app.repositories import BaseRepository
from app.db.models import ChangesHistory as ChangesHistoryModel


class ChangesHistory(BaseRepository):
    async def get_balance(self, user_id: str, timestamp: datetime) -> Optional[int]:
        query = select(ChangesHistoryModel).where(
            and_(
                ChangesHistoryModel.user_id == user_id,
                ChangesHistoryModel.operation_timestamp <= timestamp
            )
        ).order_by(
            desc(ChangesHistoryModel.operation_timestamp)
        )
        res: ChangesHistoryModel = await self.session.scalar(query)
        if not res:
            return None
        return res.balance_new
