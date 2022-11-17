from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.db.models import CommonItem as CommonItemModel
from app.repositories import CommonItem as CommonItemRepository
from app.utils.handler import AbstractHandler


class CommonItem(AbstractHandler):
    async def handle(self, item_id: str, db: Session) -> \
        Tuple[
            Optional[CommonItemRepository],
            Optional[CommonItemModel]
    ]:
        repository = CommonItemRepository(db)

        if item_id.startswith("common_"):
            id_ = item_id.removeprefix("common_")
            if not id_.isdigit():
                return repository, None
            item = await repository.get_by_id(int(id_))
            if not item:
                return repository, None
            return repository, item

        return await super().handle(item_id, db)
