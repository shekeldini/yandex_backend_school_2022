from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TEXT

from app.db import DeclarativeBase


class Specialty(DeclarativeBase):
    __tablename__ = "specialty"

    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        autoincrement=True,
        doc="Unique serial id",
    )
    name = Column(
        "name",
        TEXT,
        nullable=False,
        unique=True,
        doc="Name of specialty",
    )

    def __repr__(self) -> str:
        attributes = [
            key for key in Specialty.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )

    def __str__(self) -> str:
        attributes = [
            key for key in Specialty.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )
