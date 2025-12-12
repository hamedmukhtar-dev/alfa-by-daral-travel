from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db import get_db
from app.schemas.service_request import (
    ServiceRequestCreate,
    ServiceRequestResponse,
    ServiceRequestUpdate
)
from app.models.service_request import ServiceRequest
from app.models.user import User

from app.core.security import get_current_user, require_admin
from app.core.audit import log_admin_action
from app.config import settings


router = APIRouter(prefix="/service-requests", tags=["Service Requests"])


# -----------------------------------
# CREATE service request (Pilot aware)
# -----------------------------------
@router.post("/", response_model=ServiceRequestResponse)
async def create_service_request(
    request_data: ServiceRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Pilot guard
    if settings.PILOT_MODE and not settings.ENABLE_FREE_SERVICES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Service requests disabled in pilot mode",
        )

    new_request = ServiceRequest(
        user_id=current_user.id,
        service_type=request_data.service_type,
        description=request_data.description,
        status="pending",
    )

    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)

    return new_request


# -----------------------------------
# LIST all requests (Admin only)
# -----------------------------------
@router.get("/", response_model=List[ServiceRequestResponse])
async def list_requests(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    result = await db.execute(
        select(ServiceRequest).order_by(ServiceRequest.id.desc())
    )
    return result.scalars().all()


# -----------------------------------
# UPDATE request status (Admin only)
# -----------------------------------
@router.put("/{request_id}", response_model=ServiceRequestResponse)
async def update_request_status(
    request_id: int,
    update_data: ServiceRequestUpdate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.id == request_id)
    )
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # Soft-lock
    if req.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Service request already processed",
        )

    update_fields = update_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(req, key, value)

    await db.commit()
    await db.refresh(req)

    # Audit
    await log_admin_action(
        db,
        admin_id=admin_user.id,
        action="update_service_request",
        target_type="service_request",
        target_id=req.id,
        description=f"Updated status to {req.status}",
    )

    return req


# -----------------------------------
# GET single request (Admin or Owner)
# -----------------------------------
@router.get("/{request_id}", response_model=ServiceRequestResponse)
async def get_request(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.id == request_id)
    )
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # Admin OR Owner
    if current_user.role != "admin" and req.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    return req
