from fastapi import FastAPI
from .containers import Container
from src.routes.auth import router as auth_router
from src.routes.user import router as user_router


def include_healthcheck(app: FastAPI):
    @app.get("/healthcheck")
    async def healthcheck():
        return {"status": "ok"}


def create_app() -> FastAPI:
    api_v1_prefix = "/api/v1"

    container = Container()
    modules_to_wire = [
        'src.routes.auth',
        'src.routes.user'
    ]
    container.wire(modules=modules_to_wire)

    app = FastAPI()
    app.container = container

    include_healthcheck(app)

    app.include_router(auth_router, prefix=api_v1_prefix)
    app.include_router(user_router, prefix=api_v1_prefix)

    return app