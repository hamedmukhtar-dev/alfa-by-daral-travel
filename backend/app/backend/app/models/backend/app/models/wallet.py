from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from ..db import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Numeric(18, 2), default=0)

    user = relationship("User", backref="wallet")
