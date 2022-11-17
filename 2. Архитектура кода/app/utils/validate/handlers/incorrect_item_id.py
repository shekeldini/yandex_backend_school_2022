from app.schemas import Status
from app.utils.validate.handlers import ValidateHandler


class IncorrectItemId(ValidateHandler):
    async def handle(self, *args, **kwargs) -> Status:
        item_id = kwargs.get("item_id")
        if not item_id[item_id.find("_") + 1:].isdigit():
            return Status.INCORRECT_ITEM_ID
        else:
            return await super().handle(*args, **kwargs)
