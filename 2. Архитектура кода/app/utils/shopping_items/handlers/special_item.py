from typing import Tuple, Optional
from sqlalchemy.orm import Session

from app.db.models import SpecialItem as SpecialItemModel
from app.repositories import SpecialItem as SpecialItemRepository
from app.utils.handler import AbstractHandler


class SpecialItem(AbstractHandler):
    async def handle(self, item_id: str, db: Session) -> \
        Tuple[
            Optional[SpecialItemRepository],
            Optional[SpecialItemModel]
    ]:
        repository = SpecialItemRepository(db)

        if item_id.startswith("special_"):
            id_ = item_id.removeprefix("special_")
            if not id_.isdigit():
                return repository, None
            item = await repository.get_by_id(int(id_))
            if not item:
                return repository, None
            return repository, item

        return await super().handle(item_id, db)
