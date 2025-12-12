from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models.service_listing import ServiceListing

router = APIRouter(prefix="/public/services", tags=["Public"])


@router.get("/")
async def list_public_services(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ServiceListing)
        .where(ServiceListing.status == "active")
        .order_by(ServiceListing.created_at.desc())
    )
    return result.scalars().all()
