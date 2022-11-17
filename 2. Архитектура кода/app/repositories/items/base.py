from abc import ABC, abstractmethod
from typing import Optional, Any, Tuple

from sqlalchemy.orm import Session
from app.repositories.accounts import BaseRepository as AccountsRepository
from app.schemas import Status


class ItemInterface(ABC):
    @abstractmethod
    async def get_by_id(self, id_user: int) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    async def can_buy(
        self,
        accounts_repository: AccountsRepository,
        user: Any,
        item: Any
    ) -> Tuple[bool, Status]:
        raise NotImplemented


class BaseRepository(ItemInterface):
    def __init__(self, database: Session):
        self.database = database

    @abstractmethod
    async def get_by_id(self, item_id: int) -> Optional[Any]:
        raise NotImplemented

    @abstractmethod
    async def can_buy(
        self,
        accounts_repository: AccountsRepository,
        user: Any,
        item: Any
    ) -> Tuple[bool, Status]:
        raise NotImplemented
