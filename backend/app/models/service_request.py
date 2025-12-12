from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from app.db import Base


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)

    category = Column(String, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_name = Column(String, nullable=True)
    user_phone = Column(String, nullable=False)

    listing_id = Column(Integer, ForeignKey("service_listings.id"), nullable=True)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    source = Column(String, default="manual")  # free_api | supplier | manual

    city_from = Column(String, nullable=True)
    city_to = Column(String, nullable=True)

    price_offer = Column(Float, nullable=True)

    # 🔥 AI Intent Scoring
    intent_score = Column(String, default="medium")  
    # high | medium | low

    status = Column(String, default="pending")
    assigned_to = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
