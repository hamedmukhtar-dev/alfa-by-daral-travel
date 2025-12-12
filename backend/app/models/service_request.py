from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from app.db import Base


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)

    # -----------------------------
    # Core request info
    # -----------------------------
    category = Column(String, index=True)  # flight, hotel, car, delivery, umrah, etc.
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # -----------------------------
    # User info (Backward compatible)
    # -----------------------------
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_name = Column(String, nullable=True)
    user_phone = Column(String, nullable=False)

    # -----------------------------
    # Marketplace linkage
    # -----------------------------
    listing_id = Column(Integer, ForeignKey("service_listings.id"), nullable=True)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    source = Column(String, default="manual")  # free_api | supplier | manual

    # -----------------------------
    # Location / route
    # -----------------------------
    city_from = Column(String, nullable=True)
    city_to = Column(String, nullable=True)

    # -----------------------------
    # Commercial
    # -----------------------------
    price_offer = Column(Float, nullable=True)

    # -----------------------------
    # Lifecycle
    # -----------------------------
    status = Column(
        String,
        default="pending"
    )  # pending, in_progress, completed, canceled

    assigned_to = Column(String, nullable=True)  # agent / company name

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
