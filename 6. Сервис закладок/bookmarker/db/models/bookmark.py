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
    # ERROR: мы продолжаем хранить закладки после удаления пользователя.
    # Чтобы закладки удалялись вместе с пользователем, нужно заменить SET NULL на CASCADE.
    owner_id = Column(
        "owner_id",
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
        doc="Identifier of user, who own bookmark",
    )
    # ERROR: аналогичная проблема наблюдается с тегами - мы никогда их не удаляем.
    # Как вариант, можно пытаться удалять связанный тег, каждый раз, когда удаляется закладка.
    # Также можно, например, удалять теги, которые давно не используются периодиком.
    tag = Column(
        "tag",
        ForeignKey("tag.name"),
        nullable=True,
        server_default=text("null"),
        doc="Identifier of tag",
    )
