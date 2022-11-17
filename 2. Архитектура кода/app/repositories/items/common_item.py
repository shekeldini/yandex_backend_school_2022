from typing import Optional, Union, Tuple

from app.repositories.items import BaseRepository as ItemRepository
from app.repositories.accounts import BaseRepository as AccountsRepository
from app.repositories import DoctorAccount as DoctorAccountRepository
from app.repositories import UserAccount as UserAccountRepository

from app.db.models import DoctorAccount as DoctorAccountModel
from app.db.models import UserAccount as UserAccountModel
from app.db.models import CommonItem as CommonItemModel

from app.schemas import Status


class CommonItem(ItemRepository):
    async def get_by_id(self, item_id: int) -> Optional[CommonItemModel]:
        item = self.database.query(CommonItemModel).where(
            CommonItemModel.id == item_id
        ).first()
        if not item:
            return None
        return item

    async def can_buy(
        self,
        accounts_repository: AccountsRepository,
        user: Union[DoctorAccountModel, UserAccountModel],
        item: CommonItemModel
    ) -> Tuple[bool, Status]:
        if isinstance(accounts_repository, DoctorAccountRepository):
            return await self._doctor()
        elif isinstance(accounts_repository, UserAccountRepository):
            return await self._user()

    @staticmethod
    async def _user() -> Tuple[bool, Status]:
        return True, Status.OK

    @staticmethod
    async def _doctor() -> Tuple[bool, Status]:
        return True, Status.OK
