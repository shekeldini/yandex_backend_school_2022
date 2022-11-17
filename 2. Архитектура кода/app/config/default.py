from os import environ

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "")
    APP_HOST: str = environ.get("APP_HOST", "http://127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))

    DB_NAME: str = environ.get("DB_NAME", "pharmacy")
    DB_PATH: str = environ.get("DB_PATH", "localhost")
    DB_USER: str = environ.get("DB_USER", "student")
    DB_PORT: int = int(environ.get("DB_PORT", 5431))
    DB_PASSWORD: str = environ.get("DB_PASSWORD", "shbr2022")
    DB_POOL_SIZE: int = int(environ.get("DB_POOL_SIZE", 15))
    DB_CONNECT_RETRY: int = int(environ.get("DB_CONNECT_RETRY", 20))

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.DB_NAME,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_PATH,
            "port": self.DB_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )
