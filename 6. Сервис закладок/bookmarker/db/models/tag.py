from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT

from .base import BaseTable


class Tag(BaseTable):
    __tablename__ = "tag"

    name = Column(
        "name",
        TEXT,
        nullable=False,
        unique=True,
        index=True,
        doc="Name of the tag",
    )
