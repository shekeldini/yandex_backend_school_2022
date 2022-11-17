from bookmarker.endpoints.auth import api_router as auth_router
from bookmarker.endpoints.bookmark import api_router as bookmarks_router
from bookmarker.endpoints.ping import api_router as application_health_router


list_of_routes = [
    application_health_router,
    auth_router,
    bookmarks_router,
]


__all__ = [
    "list_of_routes",
]
