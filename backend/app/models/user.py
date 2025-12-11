from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)

    role = Column(String, default="user")  # user, agent, admin, superadmin
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
