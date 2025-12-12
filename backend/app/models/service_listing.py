from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from app.db import Base


class ServiceListing(Base):
    __tablename__ = "service_listings"

    id = Column(Integer, primary_key=True, index=True)

    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    category = Column(String, index=True)  # travel, hotel, umrah, delivery, car, local
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    city = Column(String, nullable=True)
    country = Column(String, nullable=True)

    price_from = Column(Float, nullable=True)
    price_to = Column(Float, nullable=True)
    currency = Column(String, default="USD")

    status = Column(String, default="active")  # active / paused

    created_at = Column(DateTime(timezone=True), server_default=func.now())
