from os import environ
from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = environ.get("ENV", "local")
    APP_HOST: str = environ.get("APP_HOST", "localhost")
    APP_PORT: int = int(environ.get("APP_PORT", 8000))

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", 5432))
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "")

    APPROVE_SERVICE_HOST: str = environ.get("APPROVE_SERVICE_HOST", "localhost")
    APPROVE_SERVICE_PORT: int = environ.get("APPROVE_SERVICE_PORT", 7000)

    DATE_TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.000Z"

    SERVICE_NAME: str = "Balance Manager"

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )
    @property
    def approve_url(self) -> str:
        return f"http://{self.APPROVE_SERVICE_HOST}:{self.APPROVE_SERVICE_PORT}/approve"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
