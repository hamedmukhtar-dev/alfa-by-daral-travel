from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_db
from app.models.service_request import ServiceRequest
from app.schemas.service_request import ServiceRequestOut

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.get("/requests", response_model=list[ServiceRequestOut])
async def list_requests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ServiceRequest))
    return result.scalars().all()

@router.post("/requests/{request_id}/approve")
async def approve_request(request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.id == request_id)
    )
    request = result.scalar_one_or_none()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.status = "approved"
    await db.commit()

    return {"status": "approved", "request_id": request_id}

@router.post("/requests/{request_id}/reject")
async def reject_request(request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.id == request_id)
    )
    request = result.scalar_one_or_none()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.status = "rejected"
    await db.commit()

    return {"status": "rejected", "request_id": request_id}
