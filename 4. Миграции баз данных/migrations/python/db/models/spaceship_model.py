from sqlalchemy import Column, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, DOUBLE_PRECISION

from migrations.python.db import DeclarativeBase


class SpaceshipModel(DeclarativeBase):
    __tablename__ = "spaceship_model"

    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        nullable=False
    )
    manufacturer_id = Column(
        "manufacturer_id",
        INTEGER,
        ForeignKey("spaceship_manufacturer.id"),
        nullable=False,
    )
    model_name = Column(
        "model_name",
        VARCHAR(50),
        nullable=True,
    )
    horsepower = Column(
        "horsepower",
        DOUBLE_PRECISION,
        nullable=False
    )
    __table_args__ = (
        CheckConstraint(horsepower.between(170000000, 240000000), name="valid_values"),
    )

    def __repr__(self) -> str:
        attributes = [
            key for key in SpaceshipModel.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )

    def __str__(self) -> str:
        attributes = [
            key for key in SpaceshipModel.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )
