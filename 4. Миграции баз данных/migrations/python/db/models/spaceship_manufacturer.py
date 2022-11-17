from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from migrations.python.db import DeclarativeBase


class SpaceshipManufacturer(DeclarativeBase):
    __tablename__ = "spaceship_manufacturer"

    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        nullable=False
    )
    company_name = Column(
        "company_name",
        VARCHAR(50),
        nullable=False,
    )
    country = Column(
        "country",
        VARCHAR(50),
        nullable=True,
    )
    moex_code = Column(
        "moex_code",
        VARCHAR(50),
        nullable=True,
    )

    def __repr__(self) -> str:
        attributes = [
            key for key in SpaceshipManufacturer.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )

    def __str__(self) -> str:
        attributes = [
            key for key in SpaceshipManufacturer.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )
