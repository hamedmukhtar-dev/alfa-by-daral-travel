from sqlalchemy import Column, Integer, String, DateTime, func
from app.db import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    type = Column(String, index=True)
    # feedback_high_risk | feedback_spike | high_intent_request

    severity = Column(String)
    # info | warning | critical

    message = Column(String, nullable=False)
    source_id = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
