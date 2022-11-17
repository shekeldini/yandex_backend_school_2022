from datetime import datetime
from uuid import uuid4

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChangesHistory as ChangesHistoryModel
from app.models.requests import ChangeBalance as RequestsChangeBalanceModel
from app.repositories import UserBalance as UserBalanceRepository


class ChangeBalance:
    async def change_balance(self, model: RequestsChangeBalanceModel, session: AsyncSession):
        balance_old, balance_new, user = await self._update_balance(
            user_id=model.userId,
            balance_delta=model.balanceChange,
            session=session
        )
        history = await self._create_history(
            user_id=model.userId,
            balance_delta=model.balanceChange,
            context=model.context,
            balance_old=balance_old,
            balance_new=balance_new,
            timestamp=model.timestamp,
        )
        try:
            user.balance = balance_new
            session.add(history)
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()
            return False
        return True

    @staticmethod
    async def _update_balance(user_id: str, balance_delta: int, session: AsyncSession):
        repository = UserBalanceRepository(session)
        user = await repository.get_by_id(user_id)
        balance_old = user.balance
        balance_new = balance_old + balance_delta
        return balance_old, balance_new, user

    @staticmethod
    async def _create_history(
            user_id: str,
            balance_delta: int,
            context: str,
            balance_old: int,
            balance_new: int,
            timestamp: datetime,
    ) -> ChangesHistoryModel:
        history = ChangesHistoryModel(
            id=str(uuid4()),
            context=context,
            user_id=user_id,
            balance_change=balance_delta,
            balance_old=balance_old,
            balance_new=balance_new,
            operation_timestamp=timestamp
        )
        return history


async def change_balance(model: RequestsChangeBalanceModel, session: AsyncSession) -> bool:
    obj = ChangeBalance()
    return await obj.change_balance(model, session)
