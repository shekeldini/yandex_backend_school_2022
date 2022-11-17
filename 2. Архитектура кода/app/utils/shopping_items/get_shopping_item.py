from typing import Tuple, Any, Optional
from sqlalchemy.orm import Session

from app.repositories.items import BaseRepository
from app.utils.shopping_items import SpecialItem, ReceiptItem, CommonItem


async def get_shopping_item(item_id: str, db: Session) -> Tuple[Optional[BaseRepository], Any]:
    """
    Обычно клиентский код приспособлен для работы с единственным обработчиком. В
    большинстве случаев клиенту даже неизвестно, что этот обработчик является
    частью цепочки.
    """
    special = SpecialItem()
    receipt = ReceiptItem()
    common = CommonItem()

    # создание цепочки
    special.set_next(receipt).set_next(common)

    repositories, item = await special.handle(item_id, db)
    return repositories, item
