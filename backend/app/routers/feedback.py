from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.core.security import get_current_user
from app.ai.feedback_analyzer import analyze_feedback
from app.core.alerts import create_alert

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(
    data: FeedbackCreate,
    db: AsyncSession = Depends(get_db),
):
    ai = await analyze_feedback(data.message)

    item = Feedback(
        message=data.message,
        user_name=data.user_name,
        user_contact=data.user_contact,
        ai_category=ai.get("category"),
        ai_sentiment=ai.get("sentiment"),
        ai_priority=ai.get("priority"),
    )

    db.add(item)
    await db.commit()
    await db.refresh(item)

    # 🚨 Automation: High-risk feedback
    if item.ai_priority == "high" or item.ai_category == "risk":
        await create_alert(
            db=db,
            type="feedback_high_risk",
            severity="critical",
            message="High-risk feedback detected",
            source_id=item.id,
        )

    return item


@router.get("/", response_model=list[FeedbackResponse])
async def list_feedback(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    result = await db.execute(
        select(Feedback).order_by(Feedback.created_at.desc())
    )
    return result.scalars().all()
