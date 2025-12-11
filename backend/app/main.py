from fastapi import FastAPI

from app.core.logging_config import setup_logging
from app.core.middleware import setup_middleware

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.wallet import router as wallet_router
from app.routers.service_request import router as service_router
from app.routers.admin import router as admin_router
from app.routers.ai import router as ai_router
from app.routers.travel import router as travel_router

from app.db import engine, Base
import asyncio


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="ALFA by Daral Travel",
        version="1.0.0",
        description="Unified AI Travel & Services Platform by Daral Travel",
    )

    setup_middleware(app)

    # Routers
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(wallet_router)
    app.include_router(service_router)
    app.include_router(admin_router)
    app.include_router(ai_router)
    app.include_router(travel_router)

    @app.get("/")
    async def root():
        return {
            "message": "ALFA Backend Running ✅",
            "status": "ok",
        }

    return app


app = create_app()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_db())
