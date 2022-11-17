import requests
from app.services.validate_change_balance.handlers import AbstractHandler
from app.config.utils import get_settings


class Approve(AbstractHandler):
    async def handle(self, *args, **kwargs) -> bool:
        user_id = kwargs.get("userId")
        balance_change = kwargs.get("balanceChange")
        if not (user_id and balance_change):
            return False
        settings = get_settings()
        res = await self.get_approve(
            url=settings.approve_url,
            params={
                "userId": user_id,
                "balanceChange": balance_change
            }
        )
        if res.status_code != 200:
            return False
        else:
            return await super().handle(*args, **kwargs)

    @staticmethod
    async def get_approve(url, params):
        return requests.get(
            url=url,
            params=params
        )
