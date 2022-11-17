from app.services import Context, statistic, ServiceRegistry
from app.services.strategies import RoundRobin
from app.config import Config


def get_context() -> Context:
    for service in Config().get_service_list():
        statistic.set_service(service)
    return Context(
        strategy=RoundRobin(
            available_services=ServiceRegistry(
                statistic.get_services_list()
            ).get_alive_services(),
            statistics=statistic
        ),

    )
