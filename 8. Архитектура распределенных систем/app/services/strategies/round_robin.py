import datetime
from typing import Union, Any, Tuple
from fastapi import status
from requests.exceptions import ReadTimeout, ConnectTimeout
from app.models.others import TimeOut, CreateToken, Statistic as StatisticModel
from app.services.statistic import Statistic
from app.services.strategies import BaseStrategy
from app.utils import get_settings
import requests


class RoundRobin(BaseStrategy):
    def __init__(self, available_services: list, statistics: Statistic):
        self._counter = 0
        self._available_services = self._sort_services(
            available_services,
            statistics.get_statistic()
        )
        self._statistics = statistics
        self._max_retry = get_settings().MAX_RETRY

    @staticmethod
    def _sort_services(services: list, statistics: dict) -> list:
        return sorted(
            services,
            key=lambda x: statistics[x]["trips_to_microservice"]
        )

    async def get_data(
            self,
            url_suffix: str,
            response_type: str,
            method: str,
            params: dict = None,
            data: dict = None
    ) -> Tuple[int, Any]:
        status_code, response_data = None, None
        while status_code != status.HTTP_200_OK:
            if self._counter == self._max_retry:
                return status.HTTP_503_SERVICE_UNAVAILABLE, "Service Unavailable"

            service = self.get_current_service()
            response = await self.create_request(
                method=method,
                service=service,
                params=params,
                suffix=url_suffix,
                data=data
            )
            status_code = response.status_code
            response_data = getattr(response, response_type)

            await self._statistics.write_statistic(
                StatisticModel(
                    service=service,
                    status_code=status_code,
                    data=response_data,
                    date=datetime.datetime.now()
                )
            )
            self._counter += 1
        return status_code, response_data

    async def create_token(self, params: CreateToken) -> Tuple[int, str]:
        status_code, response_data = await self.get_data(
            params=params.to_dict(),
            url_suffix="token",
            response_type="text",
            method="get"
        )
        return status_code, response_data.replace('"', '')

    def get_current_service(self):
        return self._available_services[self._counter % len(self._available_services)]

    @staticmethod
    async def create_request(
            service: str,
            params: dict,
            suffix: str,
            method: str,
            data: dict
    ) -> Union[requests.Response, TimeOut]:
        try:
            r = requests.request(
                method=method,
                url=service + suffix,
                params=params,
                timeout=(0.2, 0.2),
                data=data
            )
            return r
        except ReadTimeout:
            return TimeOut(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                text="Read TimeOut"
            )
        except ConnectTimeout:
            return TimeOut(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                text="Connect TimeOut"
            )
