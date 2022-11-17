from typing import Optional, Union, Tuple

from app.repositories.items import BaseRepository as ItemRepository
from app.repositories.accounts import BaseRepository as AccountsRepository

from app.repositories import DoctorAccount as DoctorAccountRepository
from app.repositories import UserAccount as UserAccountRepository

from app.db.models import DoctorAccount as DoctorAccountModel
from app.db.models import UserAccount as UserAccountModel
from app.db.models import SpecialItem as SpecialItemModel
from app.schemas import Status


class SpecialItem(ItemRepository):
    async def get_by_id(self, item_id: int) -> Optional[SpecialItemModel]:
        item = self.database.query(SpecialItemModel).where(
            SpecialItemModel.id == item_id
        ).first()
        if not item:
            return None
        return item

    async def can_buy(
        self,
        accounts_repository: AccountsRepository,
        user: Union[DoctorAccountModel, UserAccountModel],
        item: SpecialItemModel
    ) -> Tuple[bool, Status]:
        if isinstance(accounts_repository, DoctorAccountRepository):
            return await self._doctor(user, item)
        elif isinstance(accounts_repository, UserAccountRepository):
            return await self._user()

    @staticmethod
    async def _user() -> Tuple[bool, Status]:
        return False, Status.ITEM_IS_SPECIAL

    @staticmethod
    async def _doctor(user: DoctorAccountModel, item: SpecialItemModel) -> Tuple[bool, Status]:
        can = bool(user.specialty_id == item.specialty_id)
        if can:
            return True, Status.OK
        return False, Status.ITEM_SPECIAL_WRONG_SPECIFIC
