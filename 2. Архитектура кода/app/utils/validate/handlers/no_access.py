from app.schemas import Status
from app.utils.validate.handlers import ValidateHandler


class NoAccess(ValidateHandler):
    async def handle(self, *args, **kwargs) -> Status:
        user_repository = kwargs.get("user_repository")
        user = kwargs.get("user")
        item = kwargs.get("item")
        item_repository = kwargs.get("item_repository")
        can, massage = await item_repository.can_buy(user_repository, user, item)
        if not can:
            return massage
        else:
            return await super().handle()
