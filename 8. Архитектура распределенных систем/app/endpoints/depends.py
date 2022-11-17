from fastapi import status
from app.services import Context, statistic
from app.utils import get_settings
from app.models.others import Strategy
from app.services.strategies import RoundRobin
from app.exceptions import NoOneAvailableService, InvalidStrategy


def get_context() -> Context:
    setting = get_settings()
    alive_services = statistic.get_services_list()
    if not alive_services:
        raise NoOneAvailableService(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable try later"
        )
    if setting.STRATEGY == Strategy.ROUND_ROBIN.value:
        return Context(
            strategy=RoundRobin(
                available_services=alive_services,
                statistics=statistic
            )
        )
    else:
        raise InvalidStrategy(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid balance method name"
        )
