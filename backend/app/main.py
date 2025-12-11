from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging_config import setup_logging
from app.core.middleware import RequestLoggingMiddleware

from app.routers.auth import router as auth_router
from app.routers.wallet import router as wallet_router
from app.routers.service_request import router as service_router
from app.routers.services import router as ai_service_router  # AI Intent Router

from app.db import engine, Base
import logging


# -----------------------------
# Initialize App
# -----------------------------
def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="ALFA — Unified AI Travel & Services Platform",
        version="1.0.0",
        description="Backend API for ALFA by Daral Travel"
    )

    # Middleware
    app.add_middleware(RequestLoggingMiddleware)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(wallet_router, prefix="/wallet", tags=["Wallet"])
    app.include_router(service_router, prefix="/services", tags=["Service Requests"])
    app.include_router(ai_service_router, prefix="/ai", tags=["AI Intent Engine"])

    @app.get("/")
    async def root():
        return {"message": "ALFA Backend Running Successfully 🚀"}

    return app


app = create_app()


# -----------------------------
# Database Setup
# -----------------------------
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

import asyncio
asyncio.run(init_db())
