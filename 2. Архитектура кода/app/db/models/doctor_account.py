from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TEXT

from app.db import DeclarativeBase


class DoctorAccount(DeclarativeBase):
    __tablename__ = "doctor_account"

    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
    )
    full_name = Column(
        "full_name",
        TEXT,
        nullable=False,
    )
    phone = Column(
        "phone",
        TEXT,
        nullable=False,
        unique=True
    )
    password_hash = Column(
        "password_hash",
        TEXT,
        nullable=False,
    )
    specialty_id = Column(
        "specialty_id",
        INTEGER,
        nullable=False,
    )

    def __repr__(self) -> str:
        attributes = [
            key for key in DoctorAccount.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )

    def __str__(self) -> str:
        attributes = [
            key for key in DoctorAccount.__dict__.keys()
            if not (key.startswith("__") or key.startswith("_"))
        ]
        return (
            f"{self.__tablename__}: {', '.join([f'{key}={self.__getattribute__(key)}' for key in attributes])}"
        )
