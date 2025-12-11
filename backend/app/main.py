from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import init_db
from app.core.logging_config import setup_logging
from app.core.middleware import add_correlation_middleware
from app.core.exceptions import register_exception_handlers

# Routers
from app.routers.auth import router as auth_router
from app.routers.wallet import router as wallet_router
from app.routers.services import router as services_router

# AI Engine
from app.ai.intent_router import intent_router


def create_app() -> FastAPI:
    """Factory to build the ALFA backend application."""

    setup_logging()

    app = FastAPI(
        title="ALFA by Daral Travel",
        version="1.0.0",
        description="Unified AI Travel & Services Distribution Platform"
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Correlation IDs
    add_correlation_middleware(app)

    # Exceptions
    register_exception_handlers(app)

    # Routers
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(wallet_router, prefix="/wallet", tags=["Wallet"])
    app.include_router(services_router, prefix="/services", tags=["Services"])
    app.include_router(intent_router, prefix="/ai", tags=["AI Engine"])

    return app


app = create_app()


@app.on_event("startup")
async def on_startup():
    await init_db()
    print("🚀 ALFA Backend Started Successfully")


@app.get("/")
async def root():
    return {
        "message": "Welcome to ALFA by Daral Travel",
        "status": "running"
    }
