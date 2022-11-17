from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import ColumnProperty
from migrations.python.db import DeclarativeBase


class Driver(DeclarativeBase):
    __tablename__ = "driver"

    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        nullable=False
    )
    login = Column(
        "login",
        VARCHAR(50),
        nullable=False,
        unique=True
    )
    city = Column(
        "city",
        VARCHAR(30),
        nullable=True,
    )
    full_name = Column(
        "full_name",
        VARCHAR(255),
        nullable=False
    )

    def __repr__(self) -> str:
        attributes = [
            key for key in Driver.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )

    def __str__(self) -> str:
        attributes = [
            key for key in Driver.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )