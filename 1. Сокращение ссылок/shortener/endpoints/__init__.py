from shortener.endpoints.delete_link import api_router as delete_link_router
from shortener.endpoints.get_info_about_link import api_router as get_info_router
from shortener.endpoints.health_check import api_router as health_check_router
from shortener.endpoints.make_shorter import api_router as make_shorter_router
from shortener.endpoints.redirect_to_long import api_router as redirect_to_long_router
from shortener.endpoints.make_qr import api_router as make_qr_router


list_of_routes = [
    health_check_router,
    make_shorter_router,
    redirect_to_long_router,
    delete_link_router,
    get_info_router,
    make_qr_router
]


__all__ = [
    "list_of_routes",
]
