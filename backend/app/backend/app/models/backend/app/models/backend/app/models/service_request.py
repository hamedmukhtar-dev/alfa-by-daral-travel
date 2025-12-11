from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type = Column(String(50), nullable=False)  # travel / ebox / marketplace / city_service
    status = Column(String(50), default="pending")
    payload = Column(String, nullable=True)  # JSON as string (for simplicity)

    user = relationship("User", backref="service_requests")
