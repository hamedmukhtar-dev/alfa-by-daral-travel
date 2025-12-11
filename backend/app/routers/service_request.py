from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db import get_db
from app.schemas.service_request import (
    ServiceRequestCreate,
    ServiceRequestResponse,
    ServiceRequestUpdate
)
from app.models.service_request import ServiceRequest
from app.core.security import get_current_user


router = APIRouter()


# -----------------------------------
# CREATE service request (public)
# -----------------------------------
@router.post("/", response_model=ServiceRequestResponse)
async def create_service_request(
    request_data: ServiceRequestCreate,
    db: AsyncSession = Depends(get_db)
):
    new_request = ServiceRequest(**request_data.dict())
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
    user=Depends(get_current_user)
):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    result = await db.execute(
        ServiceRequest.__table__.select().order_by(ServiceRequest.id.desc())
    )
    return result.fetchall()


# -----------------------------------
# UPDATE request status (Admin)
# -----------------------------------
@router.put("/{request_id}", response_model=ServiceRequestResponse)
async def update_request_status(
    request_id: int,
    update_data: ServiceRequestUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(
        ServiceRequest.__table__.select().where(ServiceRequest.id == request_id)
    )
    req = result.fetchone()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    update_fields = update_data.dict(exclude_unset=True)

    await db.execute(
        ServiceRequest.__table__.update()
        .where(ServiceRequest.id == request_id)
        .values(**update_fields)
    )
    await db.commit()

    result = await db.execute(
        ServiceRequest.__table__.select().where(ServiceRequest.id == request_id)
    )
    return result.fetchone()


# -----------------------------------
# GET single request (Admin / Owner)
# -----------------------------------
@router.get("/{request_id}", response_model=ServiceRequestResponse)
async def get_request(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(
        ServiceRequest.__table__.select().where(ServiceRequest.id == request_id)
    )
    req = result.fetchone()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # Admin OR Owner can view
    if user.role != "admin" and req.user_phone != user.phone:
        raise HTTPException(403, "Not authorized")

    return req
