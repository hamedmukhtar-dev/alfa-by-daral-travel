from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db import get_db
from app.models.feedback import Feedback
from app.core.security import get_current_user

router = APIRouter(prefix="/analytics/feedback", tags=["Feedback Analytics"])


@router.get("/")
async def feedback_analytics(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    # Aggregations
    category_rows = await db.execute(
        select(Feedback.ai_category, func.count(Feedback.id))
        .group_by(Feedback.ai_category)
    )

    sentiment_rows = await db.execute(
        select(Feedback.ai_sentiment, func.count(Feedback.id))
        .group_by(Feedback.ai_sentiment)
    )

    priority_rows = await db.execute(
        select(Feedback.ai_priority, func.count(Feedback.id))
        .group_by(Feedback.ai_priority)
    )

    # Latest feedback
    latest_rows = await db.execute(
        select(Feedback)
        .order_by(Feedback.created_at.desc())
        .limit(20)
    )

    return {
        "by_category": [
            {"category": c, "count": n} for c, n in category_rows.all()
        ],
        "by_sentiment": [
            {"sentiment": s, "count": n} for s, n in sentiment_rows.all()
        ],
        "by_priority": [
            {"priority": p, "count": n} for p, n in priority_rows.all()
        ],
        "latest": [
            {
                "id": f.id,
                "message": f.message,
                "ai_category": f.ai_category,
                "ai_sentiment": f.ai_sentiment,
                "ai_priority": f.ai_priority,
                "created_at": f.created_at,
            }
            for f in latest_rows.scalars().all()
        ],
    }
