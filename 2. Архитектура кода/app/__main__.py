from logging import getLogger

from fastapi import FastAPI

from app.config import DefaultSettings
from app.db.connection import SessionManager
from app.endpoints import list_of_routes
from app.utils import get_settings

logger = getLogger(__name__)


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def init_database() -> None:
    """
    Creates a reusable database connection.
    Check before launching the application that the database is available to it.
    """
    SessionManager()


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Микросервис, реализующий проверку корзины заказов"

    application = FastAPI(
        title="Url shortener",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="1.0.0",
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    init_database()
    return application


app = get_app()
