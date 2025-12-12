from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from app.db import get_db
from app.models.service_request import ServiceRequest
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(
    prefix="/offline-payments",
    tags=["Offline Payments"]
)


@router.post("/submit")
async def submit_offline_payment(
    service_request_id: int,
    payment_method: str,
    reference_note: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit offline payment proof (Cash / Bank Transfer / Agent Payment)
    """

    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.id == service_request_id)
    )
    service_request = result.scalar_one_or_none()

    if not service_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found",
        )

    if service_request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to pay for this request",
        )

    service_request.payment_status = "OFFLINE_SUBMITTED"
    service_request.payment_method = payment_method
    service_request.payment_reference = reference_note
    service_request.payment_submitted_at = datetime.utcnow()

    db.add(service_request)
    await db.commit()
    await db.refresh(service_request)

    return {
        "message": "Offline payment submitted successfully",
        "service_request_id": service_request.id,
        "status": service_request.payment_status,
    }


@router.get("/pending")
async def list_pending_offline_payments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Admin view: list all pending offline payments
    """

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    result = await db.execute(
        select(ServiceRequest).where(
            ServiceRequest.payment_status == "OFFLINE_SUBMITTED"
        )
    )

    requests = result.scalars().all()

    return requests


@router.post("/approve")
async def approve_offline_payment(
    service_request_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Admin approves offline payment
    """

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.id == service_request_id)
    )
    service_request = result.scalar_one_or_none()

    if not service_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request not found",
        )

    service_request.payment_status = "PAID_OFFLINE_APPROVED"
    service_request.paid_at = datetime.utcnow()

    db.add(service_request)
    await db.commit()
    await db.refresh(service_request)

    return {
        "message": "Offline payment approved",
        "service_request_id": service_request.id,
        "status": service_request.payment_status,
    }
