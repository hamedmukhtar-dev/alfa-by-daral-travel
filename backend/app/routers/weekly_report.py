from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from datetime import datetime, timedelta

from app.db import get_db
from app.models.service_request import ServiceRequest
from app.core.security import require_admin

router = APIRouter(prefix="/reports/weekly", tags=["Reports"])


@router.get("/")
async def weekly_report(
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin)
):
    since = datetime.utcnow() - timedelta(days=7)

    total = await db.scalar(
        func.count(ServiceRequest.id).select().where(
            ServiceRequest.created_at >= since
        )
    )

    high = await db.scalar(
        func.count(ServiceRequest.id).select().where(
            ServiceRequest.created_at >= since,
            ServiceRequest.intent_score == "high"
        )
    )

    by_category = await db.execute(
        func.count(ServiceRequest.id),
    )

    top_categories = await db.execute(
        func.count(ServiceRequest.id),
    )

    # Categories
    cat_rows = await db.execute(
        ServiceRequest.__table__
        .select(
            ServiceRequest.category,
            func.count(ServiceRequest.id).label("count")
        )
        .where(ServiceRequest.created_at >= since)
        .group_by(ServiceRequest.category)
        .order_by(func.count(ServiceRequest.id).desc())
    )

    # Cities
    city_rows = await db.execute(
        ServiceRequest.__table__
        .select(
            ServiceRequest.city_from,
            func.count(ServiceRequest.id).label("count")
        )
        .where(ServiceRequest.created_at >= since)
        .group_by(ServiceRequest.city_from)
        .order_by(func.count(ServiceRequest.id).desc())
    )

    return {
        "period": "last_7_days",
        "total_requests": total or 0,
        "high_intent_requests": high or 0,
        "high_intent_percentage": (
            round((high / total) * 100, 2) if total else 0
        ),
        "top_categories": [
            {"category": r.category, "count": r.count}
            for r in cat_rows.fetchall()
        ],
        "top_cities": [
            {"city": r.city_from, "count": r.count}
            for r in city_rows.fetchall()
        ],
    }
