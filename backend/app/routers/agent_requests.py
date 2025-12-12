from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db import get_db
from app.models.service_request import ServiceRequest
from app.core.security import get_current_user

router = APIRouter(prefix="/agent/requests", tags=["Agent"])


@router.get("/")
async def list_agent_requests(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Agents only")

    result = await db.execute(
        select(ServiceRequest)
        .where(
            and_(
                ServiceRequest.status == "pending",
                ServiceRequest.intent_score.in_(["high", "medium"]),
                ServiceRequest.claimed_by.is_(None),
            )
        )
        .order_by(
            ServiceRequest.intent_score.desc(),
            ServiceRequest.id.desc()
        )
    )

    rows = result.scalars().all()

    return [
        {
            "id": r.id,
            "title": r.title,
            "category": r.category,
            "city_from": r.city_from,
            "city_to": r.city_to,
            "price_offer": r.price_offer,
            "intent_score": r.intent_score,
            "created_at": r.created_at,
        }
        for r in rows
    ]
