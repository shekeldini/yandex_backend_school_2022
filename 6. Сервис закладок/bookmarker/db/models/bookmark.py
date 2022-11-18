from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.postgresql import TEXT

from .base import BaseTable


class Bookmark(BaseTable):
    __tablename__ = "bookmark"

    title = Column(
        "title",
        TEXT,
        nullable=False,
        doc="Title of bookmark",
    )
    link = Column(
        "link",
        TEXT,
        nullable=False,
        doc="Link to resource",
    )
    owner_id = Column(
        "owner_id",
        ForeignKey("user.id", ondelete="SET NULL", onupdate="SET NULL"),
        nullable=True,
        doc="Identifier of user, who own bookmark",
    )
    tag = Column(
        "tag",
        ForeignKey("tag.name"),
        nullable=True,
        server_default=text("null"),
        doc="Identifier of tag",
    )
