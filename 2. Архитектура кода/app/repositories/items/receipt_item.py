from typing import Optional, Union, Tuple

from app.schemas import Status

from app.repositories.items import BaseRepository as ItemRepository
from app.repositories.accounts import BaseRepository as AccountsRepository
from app.repositories import DoctorAccount as DoctorAccountRepository
from app.repositories import UserAccount as UserAccountRepository

from app.db.models import DoctorAccount as DoctorAccountModel
from app.db.models import UserAccount as UserAccountModel
from app.db.models import Receipt as ReceiptModel
from app.db.models import ReceiptItem as ReceiptItemModel


class ReceiptItem(ItemRepository):
    async def get_by_id(self, item_id: int) -> Optional[ReceiptItemModel]:
        item = self.database.query(ReceiptItemModel).where(
            ReceiptItemModel.id == item_id
        ).first()
        if not item:
            return None
        return item

    async def can_buy(
        self,
        accounts_repository: AccountsRepository,
        user: Union[DoctorAccountModel, UserAccountModel],
        item: ReceiptItemModel
    ) -> Tuple[bool, Status]:
        if isinstance(accounts_repository, DoctorAccountRepository):
            return await self._doctor()
        elif isinstance(accounts_repository, UserAccountRepository):
            return await self._user(user, item)

    async def _user(self, user: UserAccountModel, item: ReceiptItemModel) -> Tuple[bool, Status]:
        item = self.database.query(ReceiptModel).filter(
            ReceiptModel.user_id == user.id,
            ReceiptModel.item_id == item.id,
        ).first()
        if item:
            return True, Status.OK
        return False, Status.NO_RECEIPT

    @staticmethod
    async def _doctor() -> Tuple[bool, Status]:
        return True, Status.OK
