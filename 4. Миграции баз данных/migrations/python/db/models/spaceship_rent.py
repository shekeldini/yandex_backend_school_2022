from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP

from migrations.python.db import DeclarativeBase


class SpaceshipRent(DeclarativeBase):
    __tablename__ = "spaceship_rent"
    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        autoincrement=True
    )
    driver_id = Column(
        "driver_id",
        INTEGER,
        ForeignKey("driver.id"),
        nullable=False
    )
    spaceship_id = Column(
        "spaceship_id",
        INTEGER,
        ForeignKey("spaceship.id"),
        nullable=False
    )
    rent_start = Column(
        "rent_start",
        TIMESTAMP,
        nullable=False,
    )
    rent_end = Column(
        "rent_end",
        TIMESTAMP,
        nullable=False,
    )

    def __repr__(self) -> str:
        attributes = [
            key for key in SpaceshipRent.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )

    def __str__(self) -> str:
        attributes = [
            key for key in SpaceshipRent.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )
