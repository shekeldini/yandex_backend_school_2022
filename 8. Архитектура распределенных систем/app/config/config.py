from os import environ
from pydantic import BaseConfig, Field
from app.models.others.strategy import Strategy


class Config(BaseConfig):
    STRATEGY: str = environ.get("STRATEGY", Strategy.ROUND_ROBIN.value)
    SERVICE_LINKS: str = environ.get("SERVICE_LINKS", "")
    DATE_TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.000Z"
    MAX_RETRY: int = Field(default=10)

    def get_service_list(self):
        return [f"http://{link}/" for link in self.SERVICE_LINKS.split(";")]

