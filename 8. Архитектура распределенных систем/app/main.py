import json

import uvicorn
from logging import getLogger
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi_utils.tasks import repeat_every
from app.endpoints import list_of_routes
from app.exceptions import exception_list, MyException
from app.services import statistic, ServiceRegistry
from app.utils import get_settings

logger = getLogger(__name__)


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route)


def add_exception_handlers(application: FastAPI):
    def exception_handler(request: Request, exc: MyException):
        return PlainTextResponse(content=exc.detail, status_code=exc.status_code)

    for exception in exception_list:
        application.add_exception_handler(exception, exception_handler)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Load Balancer"

    application = FastAPI(
        title="Load Balancer",
        description=description,
        docs_url="/docs",
        openapi_url="/openapi",
        version="1.0.0",
    )

    bind_routes(application)
    add_exception_handlers(application)
    return application


app = get_app()


@app.on_event("startup")
def startup():
    settings = get_settings()
    available_services = ServiceRegistry(
        settings.get_service_list()
    ).get_alive_services()
    for service in available_services:
        statistic.set_service(service)


@app.on_event("startup")
@repeat_every(seconds=60 * 2, wait_first=True)
def write_statistic():
    data = statistic.get_statistic()
    for key in data:
        if data[key]["responses"]:
            with open('logs/statistics', 'a') as file:
                for response in range(len(data[key]["responses"])):
                    obj = json.dumps(data[key]["responses"].pop())
                    file.write(obj + '\n')


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', reload=False)
