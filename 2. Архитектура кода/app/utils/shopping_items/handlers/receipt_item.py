from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.db.models import ReceiptItem as ReceiptItemModel
from app.repositories import ReceiptItem as ReceiptItemRepository
from app.utils.handler import AbstractHandler


class ReceiptItem(AbstractHandler):
    async def handle(self, item_id: str, db: Session) -> \
        Tuple[
            Optional[ReceiptItemRepository],
            Optional[ReceiptItemModel]
    ]:
        repository = ReceiptItemRepository(db)

        if item_id.startswith("receipt_"):
            id_ = item_id.removeprefix("receipt_")
            if not id_.isdigit():
                return repository, None
            item = await repository.get_by_id(int(id_))
            if not item:
                return repository, None
            return repository, item

        return await super().handle(item_id, db)
