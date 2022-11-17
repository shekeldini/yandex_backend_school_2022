from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Any, Tuple
from sqlalchemy.orm import Session


class Handler(ABC):
    """
    Интерфейс Обработчика объявляет метод построения цепочки обработчиков.
    Он также объявляет метод для выполнения запроса.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        raise NotImplemented

    @abstractmethod
    async def handle(self, request: Any, db: Session) -> Optional[Any]:
        raise NotImplemented


class AbstractHandler(Handler):
    """
    Поведение цепочки по умолчанию может быть реализовано внутри базового класса
    обработчика.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    async def handle(self, request: Any, db: Session) -> Tuple[Optional[Any], Optional[Any]]:
        if self._next_handler:
            return await self._next_handler.handle(request, db)
        return None, None

