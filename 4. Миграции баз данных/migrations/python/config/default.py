from os import environ

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    ENV: str = environ.get("ENV", "local")
    DB_NAME: str = environ.get("DB_NAME", "sdb_homework")
    DB_PATH: str = environ.get("DB_PATH", "postgres")
    DB_USER: str = environ.get("DB_USER", "admin")
    DB_PORT: int = int(environ.get("DB_PORT", 5432))
    DB_PASSWORD: str = environ.get("DB_PASSWORD", "admin")
    SDB_TRACK: str = str(environ.get("SDB_TRACK", "python"))

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
