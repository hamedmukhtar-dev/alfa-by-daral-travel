from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    # User content
    message = Column(Text, nullable=False)
    user_name = Column(String, nullable=True)
    user_contact = Column(String, nullable=True)

    # AI classification
    ai_category = Column(String, index=True)
    # complaint | suggestion | issue | praise | risk

    ai_sentiment = Column(String)
    # positive | neutral | negative

    ai_priority = Column(String)
    # high | medium | low

    created_at = Column(DateTime(timezone=True), server_default=func.now())
