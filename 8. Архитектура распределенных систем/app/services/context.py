from __future__ import annotations

from app.models.others import CreateToken
from app.services.strategies import BaseStrategy


class Context:
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов.
    """

    def __init__(self, strategy: BaseStrategy) -> None:
        """
        Обычно Контекст принимает стратегию через конструктор, а также
        предоставляет сеттер для её изменения во время выполнения.
        """
        self._strategy = strategy

    @property
    def strategy(self) -> BaseStrategy:
        """
        Контекст хранит ссылку на один из объектов Стратегии. Контекст не знает
        конкретного класса стратегии. Он должен работать со всеми стратегиями
        через интерфейс Стратегии.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BaseStrategy) -> None:
        """
        Обычно Контекст позволяет заменить объект Стратегии во время выполнения.
        """

        self._strategy = strategy

    async def create_token(self, request: CreateToken) -> str:
        """
        Вместо того, чтобы самостоятельно реализовывать множественные версии
        алгоритма, Контекст делегирует некоторую работу объекту Стратегии.
        """
        return await self._strategy.create_token(request)
