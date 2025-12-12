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
from app.routers.offline_payments import router as offline_payments_router
from app.routers.reports import router as reports_router  # ✅ NEW

from app.db import engine, Base


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="ALFA by Daral Travel",
        version="1.0.0",
        description="Unified AI Travel & Services Platform by Daral Travel",
    )

    setup_middleware(app)

    # --------------------
    # Routers
    # --------------------
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(wallet_router)
    app.include_router(service_router)
    app.include_router(admin_router)
    app.include_router(ai_router)
    app.include_router(travel_router)
    app.include_router(offline_payments_router)
    app.include_router(reports_router)  # ✅ STEP 5

    # --------------------
    # System Endpoints
    # --------------------
    @app.get("/")
    async def root():
        return {
            "message": "ALFA Backend Running ✅",
            "status": "ok",
        }

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    # --------------------
    # Startup
    # --------------------
    @app.on_event("startup")
    async def on
