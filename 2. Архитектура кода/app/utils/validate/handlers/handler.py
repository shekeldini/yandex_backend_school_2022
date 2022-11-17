from typing import Any, Optional

from app.schemas import Status
from app.utils.handler import AbstractHandler


class ValidateHandler(AbstractHandler):
    async def handle(self, *args, **kwargs) -> Optional[Any]:
        if self._next_handler:
            return await self._next_handler.handle(*args, **kwargs)
        return Status.OK
