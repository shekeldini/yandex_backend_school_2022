from fastapi import FastAPI
from fastapi_pagination import add_pagination
from uvicorn import run

from bookmarker.config import DefaultSettings, get_settings
from bookmarker.endpoints import list_of_routes
from bookmarker.utils.common import get_hostname


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Микросервис, реализующий возможность укорачивать ссылки."

    tags_metadata = [
        {
            "name": "Application Health",
            "description": "API health check.",
        },
    ]

    application = FastAPI(
        title="Bookmarker",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application, settings)
    add_pagination(application)
    application.state.settings = settings
    return application


app = get_app()

if __name__ == "__main__":  # pragma: no cover
    settings_for_application = get_settings()
    run(
        "bookmarker.__main__:app",
        host=get_hostname(settings_for_application.APP_HOST),
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["bookmarker", "tests"],
        log_level="debug",
    )
