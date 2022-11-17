from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from migrations.python.db import DeclarativeBase


class Spaceship(DeclarativeBase):
    __tablename__ = "spaceship"

    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        nullable=False
    )
    ship_number = Column(
        "ship_number",
        VARCHAR(50),
        nullable=False,
    )
    model_id = Column(
        "model_id",
        INTEGER,
        ForeignKey("spaceship_model.id"),
        nullable=False,
    )

    def __repr__(self) -> str:
        attributes = [
            key for key in Spaceship.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )

    def __str__(self) -> str:
        attributes = [
            key for key in Spaceship.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )
