from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.db.models import UserAccount as UserAccountModel
from app.repositories import UserAccount as UserAccountRepository
from app.utils.handler import AbstractHandler


class UserAccount(AbstractHandler):
    async def handle(self, user_id: int, db: Session) -> \
        Tuple[
            Optional[UserAccountRepository],
            Optional[UserAccountModel]
    ]:
        repository = UserAccountRepository(db)
        user = await repository.get_by_id(user_id)

        if user:
            return repository, user
        else:
            return await super().handle(user_id, db)
