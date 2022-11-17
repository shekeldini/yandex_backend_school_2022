from app.schemas import Status
from app.utils.shopping_items.get_shopping_item import get_shopping_item
from app.utils.validate.handlers import ValidateHandler


class WrongCategory(ValidateHandler):
    async def handle(self, *args, **kwargs) -> Status:
        item_id = kwargs.get("item_id")
        db = kwargs.get("db")
        item_repository, item = await get_shopping_item(item_id, db)
        if not item_repository:
            return Status.WRONG_CATEGORY
        else:
            return await super().handle(item=item, item_repository=item_repository, **kwargs)
