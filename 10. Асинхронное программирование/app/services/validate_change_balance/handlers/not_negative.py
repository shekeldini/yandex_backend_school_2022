from app.services.validate_change_balance.handlers import AbstractHandler
from app.repositories import UserBalance as UserBalanceRepository


class NotNegative(AbstractHandler):
    async def handle(self, *args, **kwargs) -> bool:
        user_id = kwargs.get("userId")
        balance_change = kwargs.get("balanceChange")
        db_session = kwargs.get("session")
        if not (user_id and balance_change and db_session):
            return False
        repository = UserBalanceRepository(db_session)
        user = await repository.get_by_id(user_id)
        if not user:
            return False
        if user.balance + balance_change < 0:
            return False
        else:
            return await super().handle(*args, **kwargs)
