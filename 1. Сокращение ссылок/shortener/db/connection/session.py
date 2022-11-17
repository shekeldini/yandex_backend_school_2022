from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from shortener.utils import get_settings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.engine = create_engine(get_settings().database_uri, pool_pre_ping=True)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance

    def get_session(self) -> Session:
        return self.session_local()

    def refresh(self) -> None:
        self.engine = create_engine(get_settings().database_uri, pool_pre_ping=True)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


def get_db() -> Session:
    database = SessionManager().get_session()
    try:
        yield database
    finally:
        database.close()


__all__ = [
    "get_db",
    "SessionManager",
]
