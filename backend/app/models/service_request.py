from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)       # delivery, travel, medicine, cargo, service
    title = Column(String)
    description = Column(String, nullable=True)

    user_name = Column(String, nullable=True)
    user_phone = Column(String)

    city_from = Column(String, nullable=True)
    city_to = Column(String, nullable=True)

    price_offer = Column(Float, nullable=True)

    status = Column(String, default="pending")  # pending, in_progress, completed, canceled
    assigned_to = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
