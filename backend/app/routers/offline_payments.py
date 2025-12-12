from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.offline_payment import OfflinePayment
from app.schemas.offline_payment import OfflinePaymentCreate
from app.core.security import get_current_user

router = APIRouter(
    prefix="/payments/offline",
    tags=["Offline Payments"]
)


@router.post("/confirm")
async def confirm_offline_payment(
    payload: OfflinePaymentCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    payment = OfflinePayment(
        user_id=user.id,
        service_request_id=payload.service_request_id,
        method=payload.method,
        reference=payload.reference,
    )

    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    return {
        "id": payment.id,
        "status": payment.status,
        "message": "Offline payment recorded successfully"
    }
