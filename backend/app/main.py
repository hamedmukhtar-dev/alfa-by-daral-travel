from fastapi import FastAPI

from app.core.logging_config import setup_logging
from app.core.middleware import setup_middleware

# --------------------
# Core Routers
# --------------------
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.wallet import router as wallet_router
from app.routers.service_request import router as service_router
from app.routers.admin import router as admin_router
from app.routers.ai import router as ai_router
from app.routers.travel import router as travel_router
from app.routers.offline_payments import router as offline_payments_router

# --------------------
# Reports & Analytics
# --------------------
from app.routers.reports import router as reports_router
from app.routers.weekly_report import router as weekly_report_router
from app.routers.feedback import router as feedback_router
from app.routers.feedback_analytics import router as feedback_analytics_router

# --------------------
# Agent Flow
# --------------------
from app.routers.agent_requests import router as agent_requests_router
from app.routers.agent_claim import router as agent_claim_router

# --------------------
# Marketplace (Supplier / Public)
# --------------------
from app.routers.supplier_listings import router as supplier_listings_router
from app.routers.public_listings import router as public_listings_router

# --------------------
# DB
# --------------------
from app.db import engine, Base


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="ALFA by Daral Travel",
        version="1.0.0",
        description="Unified AI Travel & Services Platform by Daral Travel",
    )

    setup_middleware(app)

    # =========================================================
    # Routers Registration
    # =========================================================

    # Auth & Users
    app.include_router(auth_router)
    app.include_router(users_router)

    # Core Business
    app.include_router(wallet_router)
    app.include_router(service_router)
    app.include_router(admin_router)
    app.include_router(ai_router)
    app.include_router(travel_router)
    app.include_router(offline_payments_router)

    # Reports & Analytics
    app.include_router(reports_router)
    app.include_router(weekly_report_router)
    app.include_router(feedback_router)
    app.include_router(feedback_analytics_router)

    # Agent Operations
    app.include_router(agent_requests_router)
    app.include_router(agent_claim_router)

    # Marketplace
    app.include_router(supplier_listings_router)
    app.include_router(public_listings_router)

    # =========================================================
    # System Endpoints
    # =========================================================

    @app.get("/")
    async def root():
        return {
            "message": "ALFA Backend Running ✅",
            "status": "ok",
            "mode": "pilot",
        }

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    # =========================================================
    # Startup
    # =========================================================

    @app.on_event("startup")
    async def on_startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return app


app = create_app()
