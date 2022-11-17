from app.endpoints.change_balance import api_router as change_balance_router
from app.endpoints.get_balance import api_router as get_balance_router

list_of_routes = [
    change_balance_router,
    get_balance_router
]

__all__ = [
    "list_of_routes"
]
