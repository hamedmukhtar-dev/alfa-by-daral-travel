from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models.service_listing import ServiceListing
from app.schemas.service_listing import (
    ServiceListingCreate,
    ServiceListingResponse
)
from app.core.security import get_current_user

router = APIRouter(prefix="/supplier/listings", tags=["Supplier"])


@router.post("/", response_model=ServiceListingResponse)
async def create_listing(
    data: ServiceListingCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "supplier":
        raise HTTPException(status_code=403, detail="Suppliers only")

    listing = ServiceListing(
        supplier_id=user.id,
        **data.dict()
    )

    db.add(listing)
    await db.commit()
    await db.refresh(listing)
    return listing


@router.get("/", response_model=list[ServiceListingResponse])
async def my_listings(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "supplier":
        raise HTTPException(status_code=403, detail="Suppliers only")

    result = await db.execute(
        select(ServiceListing).where(ServiceListing.supplier_id == user.id)
    )
    return result.scalars().all()
