from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, BIGINT, TIMESTAMP

from app.db import DeclarativeBase


class ChangesHistory(DeclarativeBase):
    __tablename__ = "changes_history"

    id = Column(
        "id",
        VARCHAR(50),
        primary_key=True,
        unique=True,
    )
    context = Column(
        "context",
        VARCHAR(100),
        nullable=True
    )
    user_id = Column(
        "user_id",
        ForeignKey("user_balance.user_id"),
        nullable=False,
    )
    balance_change = Column(
        "balance_change",
        BIGINT,
        nullable=False,
    )
    balance_old = Column(
        "balance_old",
        BIGINT,
        nullable=False,
    )
    balance_new = Column(
        "balance_new",
        BIGINT,
        nullable=False,
    )
    operation_timestamp = Column(
        "operation_timestamp",
        TIMESTAMP,
        nullable=False,
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
