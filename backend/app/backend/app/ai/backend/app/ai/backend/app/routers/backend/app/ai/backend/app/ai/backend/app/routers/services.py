# backend/app/routers/services.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import get_db
from backend.app.models.service_request import ServiceRequest
from backend.app.schemas.service_request import ServiceRequestCreate, ServiceRequestOut

router = APIRouter(prefix="/services", tags=["Services"])


@router.post("/", response_model=ServiceRequestOut)
async def create_service_request(payload: ServiceRequestCreate, db: AsyncSession = Depends(get_db)):
    """
    إنشاء طلب خدمة جديد (Delivery, Travel, Cargo, Pharmacy, Telco...)
    """
    new_req = ServiceRequest(
        user_id=payload.user_id,
        category=payload.category,
        description=payload.description,
        status="pending"
    )

    db.add(new_req)
    await db.commit()
    await db.refresh(new_req)

    return new_req


@router.get("/{request_id}", response_model=ServiceRequestOut)
async def get_service_request(request_id: int, db: AsyncSession = Depends(get_db)):
    """
    جلب طلب خدمة محدد
    """
    req = await db.get(ServiceRequest, request_id)
    return req


@router.get("/")
async def list_user_services(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    جلب كل طلبات مستخدم معين
    """
    result = await db.execute(
        ServiceRequest.__table__.select().where(ServiceRequest.user_id == user_id)
    )
    return result.fetchall()
