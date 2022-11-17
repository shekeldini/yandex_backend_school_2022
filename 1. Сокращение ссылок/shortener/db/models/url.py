from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, TIMESTAMP, UUID
from sqlalchemy.sql import func

from shortener.db import DeclarativeBase


class UrlStorage(DeclarativeBase):
    __tablename__ = "url_storage"

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.uuid_generate_v4(),
        unique=True,
        doc="Unique id of the string in table",
    )
    long_url = Column(
        "long_url",
        TEXT,
        nullable=False,
        index=True,
        doc="Long version of url",
    )
    short_url = Column(
        "short_url",
        TEXT,
        nullable=False,
        index=True,
        unique=True,
        doc="Suffix of short url",
    )
    secret_key = Column(
        "secret_key",
        UUID(as_uuid=True),
        index=True,
        server_default=func.uuid_generate_v4(),
        unique=True,
        doc="Secret code to access administrator features",
    )
    number_of_clicks = Column(
        "number_of_clicks",
        INTEGER,
        nullable=False,
        server_default=text("0"),
        doc="Number of clicks on the link",
    )
    number_of_use_qr_code = Column(
        "number_of_use_qr_code",
        INTEGER,
        nullable=False,
        server_default=text("0"),
        doc="Number of use qr code",
    )
    dt_created = Column(
        "dt_created",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Date and time when string in table was created",
    )
    dt_expired = Column(
        "dt_expired",
        TIMESTAMP(timezone=True),
        server_default=text("NOW() + interval '100 years'"),
        nullable=False,
        doc="Date and time when string in table be expired",
    )

    def __repr__(self) -> str:
        return (
            f"{self.__tablename__}: {self.id=}, {self.long_url=}, {self.short_url=}, {self.secret_key=}, "
            f"{self.number_of_clicks=}, {self.dt_created=}"
        )
