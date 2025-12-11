from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import get_db
from ..models.service_request import ServiceRequest
from ..schemas.service_request import ServiceRequestCreate, ServiceRequestRead
from ..core.security import get_current_user
from ..models.user import User
from ..ai.intent_router import route_request

router = APIRouter(prefix="/services", tags=["services"])


@router.post("/", response_model=ServiceRequestRead)
async def create_service_request(
    payload: ServiceRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # هنا تقدر تستخدم AI لتفسير الطلب أو تعديل payload:
    routed = await route_request(payload.service_type, payload.payload)

    req = ServiceRequest(
        user_id=current_user.id,
        service_type=routed["service_type"],
        status="pending",
        payload=routed.get("payload"),
    )
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return req


@router.get("/", response_model=list[ServiceRequestRead])
async def list_my_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ServiceRequest).where(ServiceRequest.user_id == current_user.id)
    )
    return result.scalars().all()
