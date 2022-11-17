from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER

from app.db import DeclarativeBase


class Receipt(DeclarativeBase):
    __tablename__ = "receipt"

    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
    )
    user_id = Column(
        "user_id",
        INTEGER,
        nullable=False,
        quote=True,
    )
    item_id = Column(
        "item_id",
        INTEGER,
        nullable=False,
        quote=True,
    )

    def __repr__(self) -> str:
        attributes = [
            key for key in Receipt.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )

    def __str__(self) -> str:
        attributes = [
            key for key in Receipt.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )
