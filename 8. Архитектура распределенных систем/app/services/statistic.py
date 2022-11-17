from app.models.others import Statistic as StatisticModel


class Statistic:
    def __init__(self):
        self._services = {}

    def set_service(self, service):
        self._services[service] = {
            "trips_to_microservice": 0,
            "responses": []
        }

    def get_by_service(self, service):
        return self._services[service]

    def get_statistic(self):
        return self._services

    def get_services_list(self):
        return list(self._services.keys())

    async def write_statistic(self, statistic_model: StatisticModel):
        data = self.get_by_service(statistic_model.service)
        data["trips_to_microservice"] += 1
        data["responses"].append(statistic_model.dict())


statistic = Statistic()
