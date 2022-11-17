from typing import Optional

from app.repositories.accounts import BaseRepository
from app.db.models import UserAccount as UserAccountModel


class UserAccount(BaseRepository):
    async def get_by_id(self, user_id: int) -> Optional[UserAccountModel]:
        user = self.database.query(UserAccountModel).where(
            UserAccountModel.id == user_id
        ).first()
        if not user:
            return None
        return user
