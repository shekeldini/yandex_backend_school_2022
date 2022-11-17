from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, BIGINT

from app.db import DeclarativeBase


class UserBalance(DeclarativeBase):
    __tablename__ = "user_balance"

    user_id = Column(
        "user_id",
        VARCHAR(50),
        primary_key=True,
        unique=True,
    )
    balance = Column(
        "balance",
        BIGINT,
        nullable=False
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
