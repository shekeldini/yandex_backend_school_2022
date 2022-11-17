from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TEXT

from app.db import DeclarativeBase


class SpecialItem(DeclarativeBase):
    __tablename__ = "special_item"

    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    name = Column(
        "name",
        TEXT,
        nullable=False,
    )
    amount = Column(
        "amount",
        INTEGER,
        nullable=False,
    )
    price = Column(
        "price",
        TEXT,
        nullable=False,
    )
    dosage_form = Column(
        "dosage_form",
        TEXT,
        nullable=False,
    )
    manufacturer = Column(
        "manufacturer",
        TEXT,
        nullable=False,
    )
    barcode = Column(
        "barcode",
        TEXT,
        nullable=False,
        unique=True
    )
    specialty_id = Column(
        "specialty_id",
        INTEGER,
        nullable=False
    )

    def __repr__(self) -> str:
        attributes = [
            key for key in SpecialItem.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )

    def __str__(self) -> str:
        attributes = [
            key for key in SpecialItem.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )
