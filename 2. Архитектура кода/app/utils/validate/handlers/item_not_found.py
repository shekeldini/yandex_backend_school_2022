from app.schemas import Status
from app.utils.validate.handlers import ValidateHandler


class ItemNotFound(ValidateHandler):
    async def handle(self, *args, **kwargs) -> Status:
        item = kwargs.get("item")
        if not item:
            return Status.ITEM_NOT_FOUND
        else:
            return await super().handle(*args, **kwargs)
