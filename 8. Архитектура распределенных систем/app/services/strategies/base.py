from abc import ABC, abstractmethod

from app.models.others import CreateToken


class BaseStrategy(ABC):
    @abstractmethod
    async def create_token(self, request: CreateToken) -> str:
        raise NotImplemented
