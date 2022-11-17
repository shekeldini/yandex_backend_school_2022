from enum import Enum


class BookmarksSortKey(str, Enum):
    BY_ID = "BY_ID"
    BY_DATE = "BY_DATE"
    BY_TITLE = "BY_TITLE"
    BY_LINK = "BY_LINK"
