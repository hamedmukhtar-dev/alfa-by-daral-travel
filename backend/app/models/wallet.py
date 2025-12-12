from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
import enum

class WalletTransactionType(str, enum.Enum):
    OFFLINE_CREDIT = "offline_credit"
    DEBIT = "debit"

class WalletTransactionStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, unique=True)
    balance = Column(Float, default=0.0)

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(WalletTransactionType), nullable=False)
    status = Column(Enum(WalletTransactionStatus), default=WalletTransactionStatus.PENDING)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
