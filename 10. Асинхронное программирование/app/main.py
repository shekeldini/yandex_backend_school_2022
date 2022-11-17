import uvicorn
from fastapi import FastAPI

from app.config import get_settings
from app.endpoints import list_of_routes


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Balance Manager"

    application = FastAPI(
        title="Balance Manager",
        description=description,
        docs_url="/docs",
        openapi_url="/openapi",
        version="1.0.0",
    )

    bind_routes(application)
    return application


app = get_app()


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT, reload=False)
