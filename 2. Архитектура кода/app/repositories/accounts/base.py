from abc import ABC, abstractmethod
from typing import Optional, Any

from sqlalchemy.orm import Session


class AccountInterface(ABC):
    @abstractmethod
    async def get_by_id(self, id_user: int) -> Optional[Any]:
        raise NotImplemented


class BaseRepository(AccountInterface):
    def __init__(self, database: Session):
        self.database = database

    @abstractmethod
    async def get_by_id(self, id_user: int) -> Optional[Any]:
        raise NotImplemented
