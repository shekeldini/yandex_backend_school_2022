from app.repositories import CommonItem, ReceiptItem, SpecialItem
from app.schemas import Status
from app.utils.validate.handlers import ValidateHandler


class NoUser(ValidateHandler):
    async def handle(self, *args, **kwargs) -> Status:
        user = kwargs.get("user")
        item_repository = kwargs.get("item_repository")
        if not user:
            if isinstance(item_repository, CommonItem):
                return Status.NO_USER
            elif isinstance(item_repository, ReceiptItem):
                return Status.NO_USER_NO_RECEIPT
            elif isinstance(item_repository, SpecialItem):
                return Status.NO_USER_SPECIAL_ITEM
        else:
            return await super().handle(*args, **kwargs)
