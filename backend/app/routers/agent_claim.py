from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.db import get_db
from app.models.service_request import ServiceRequest
from app.core.security import get_current_user

router = APIRouter(prefix="/agent/claim", tags=["Agent"])


@router.post("/{request_id}")
async def claim_request(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Agents only")

    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.id == request_id)
    )
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    if req.claimed_by:
        raise HTTPException(status_code=409, detail="Request already claimed")

    req.claimed_by = user.id
    req.claimed_at = datetime.utcnow()

    await db.commit()

    return {
        "status": "claimed",
        "request_id": req.id,
        "claimed_by": user.id,
    }
