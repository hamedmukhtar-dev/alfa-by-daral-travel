from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db import Base

class OfflinePayment(Base):
    __tablename__ = "offline_payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_request_id = Column(Integer, ForeignKey("service_requests.id"))

    method = Column(String, nullable=False)        # Cash / Bank / Agent
    reference = Column(String, nullable=True)      # Receipt / Ref No
    status = Column(String, default="pending")     # pending / approved

    created_at = Column(DateTime(timezone=True), server_default=func.now())
