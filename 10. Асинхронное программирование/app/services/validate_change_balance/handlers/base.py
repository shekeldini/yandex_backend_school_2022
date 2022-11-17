from __future__ import annotations
from abc import ABC, abstractmethod


class Handler(ABC):
    """
    Интерфейс Обработчика объявляет метод построения цепочки обработчиков.
    Он также объявляет метод для выполнения запроса.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        raise NotImplemented

    @abstractmethod
    async def handle(self, *args, **kwargs) -> bool:
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

    async def handle(self, *args, **kwargs) -> bool:
        if self._next_handler:
            return await self._next_handler.handle(*args, **kwargs)
        return True

