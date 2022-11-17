from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.db.models import DoctorAccount as DoctorAccountModel
from app.repositories import DoctorAccount as DoctorAccountRepository
from app.utils.handler import AbstractHandler


class DoctorAccount(AbstractHandler):
    async def handle(self, user_id: int, db: Session) -> \
        Tuple[
            Optional[DoctorAccountRepository],
            Optional[DoctorAccountModel]
    ]:
        repository = DoctorAccountRepository(db)
        user = await repository.get_by_id(user_id)

        if user:
            return repository, user
        else:
            return await super().handle(user_id, db)
