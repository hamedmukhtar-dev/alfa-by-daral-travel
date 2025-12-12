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
from app.ai.intent_scoring import score_intent
from app.core.notifications import notify_high_intent  # 🔔 NEW

router = APIRouter(prefix="/requests", tags=["Service Requests"])


# -----------------------------------
# CREATE service request
# -----------------------------------
@router.post("/", response_model=ServiceRequestResponse)
async def create_service_request(
    request_data: ServiceRequestCreate,
    db: AsyncSession = Depends(get_db)
):
    payload = request_data.dict()

    # 🧠 AI Intent Scoring
    intent = score_intent(payload)

    new_request = ServiceRequest(
        **payload,
        intent_score=intent
    )

    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)

    # 🔔 Notify admin if HIGH intent (Pilot-safe)
    if intent == "high":
        await notify_high_intent(new_request)

    return new_request


# -----------------------------------
# LIST requests (Admin only)
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
        ServiceRequest.__table__
        .select()
        .order_by(
            ServiceRequest.intent_score.desc(),
            ServiceRequest.id.desc()
        )
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

    await db.execute(
        ServiceRequest.__table__.update()
        .where(ServiceRequest.id == request_id)
        .values(**update_data.dict(exclude_unset=True))
    )
    await db.commit()

    result = await db.execute(
        ServiceRequest.__table__.select().where(ServiceRequest.id == request_id)
    )
    return result.fetchone()
