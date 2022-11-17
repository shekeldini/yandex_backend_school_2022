from app.endpoints.token import router as token_router


list_of_routes = [
    token_router
]


__all__ = [
    "list_of_routes",
]
