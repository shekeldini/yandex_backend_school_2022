from typing import Optional
from app.schemas import Status
from app.utils.validate.handlers import IncorrectItemId, ItemNotFound, NoAccess, NoUser, WrongCategory


async def can_buy(*args, **kwargs) -> Optional[Status]:
    """
    Обычно клиентский код приспособлен для работы с единственным обработчиком. В
    большинстве случаев клиенту даже неизвестно, что этот обработчик является
    частью цепочки.
    """
    incorrect_item_id = IncorrectItemId()
    wrong_category = WrongCategory()
    item_not_found = ItemNotFound()
    no_user = NoUser()
    no_access = NoAccess()

    # создание цепочки
    # incorrect_item_id.set_next(wrong_category).set_next(item_not_found).set_next(no_user).set_next(no_access)
    wrong_category.set_next(incorrect_item_id).set_next(item_not_found).set_next(no_user).set_next(no_access)
    status = await wrong_category.handle(*args, **kwargs)
    return status
