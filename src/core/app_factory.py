from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from docs.open_api_specs.routes import healthcheck as healthcheck_specs

from .containers import Container
from src.routes.auth import router as auth_router
from src.routes.user import router as user_router
from src.routes.shortened_url import router as shortened_url_router
from src.routes.public_routes import router as router_with_public_endpoints
from .settings import settings


def include_healthcheck(app: FastAPI):
    @app.get("/healthcheck", **healthcheck_specs.specs)
    async def healthcheck():
        return {"status": "ok"}

def include_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def create_app() -> FastAPI:
    api_v1_prefix = "/api/v1"

    container = Container()
    modules_to_wire = [
        'src.routes.auth',
        'src.routes.user',
        'src.routes.shortened_url',
        'src.routes.public_routes',
    ]

    container.wire(modules=modules_to_wire)

    app = FastAPI()
    app.container = container
    
    include_middlewares(app)

    include_healthcheck(app)
    app.include_router(router_with_public_endpoints)

    app.include_router(auth_router, prefix=api_v1_prefix)
    app.include_router(user_router, prefix=api_v1_prefix)
    app.include_router(shortened_url_router, prefix=api_v1_prefix)


    return app