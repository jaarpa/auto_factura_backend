import logging

from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from containers import Container
from fastapi_app.endpoints import router
from fastapi_app.middlewares.authorization import JWTAuthBackend


def create_app() -> FastAPI:
    """
    Fastapi app factory method.
    Creates an app and sets up the container for dependency injection.

    :return: Fastapi app.
    """

    container = Container()
    container.init_resources()
    logging.info("Initialized container for dependency injection")

    fastapi_app = FastAPI()
    setattr(fastapi_app, "container", container)

    fastapi_app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())

    fastapi_app.include_router(router)

    logging.info("Initialized fastapi app")
    logging.info("Fastapi app ready to accept connections")
    return fastapi_app


app = create_app()
