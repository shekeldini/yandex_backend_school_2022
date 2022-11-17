from typing import Optional

from app.repositories.accounts import BaseRepository
from app.db.models import DoctorAccount as DoctorAccountModel


class DoctorAccount(BaseRepository):
    async def get_by_id(self, user_id: int) -> Optional[DoctorAccountModel]:
        user = self.database.query(DoctorAccountModel).where(
            DoctorAccountModel.id == user_id
        ).first()
        if not user:
            return None
        return user
