from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models.wallet import Wallet, WalletTransaction, WalletTransactionType
from app.schemas.wallet import OfflineCreditRequest, WalletOut
from app.core.security import get_current_user

router = APIRouter(prefix="/wallet", tags=["Wallet"])

@router.get("/", response_model=WalletOut)
async def get_wallet(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Wallet).where(Wallet.user_id == user.id))
    wallet = result.scalar_one_or_none()

    if not wallet:
        wallet = Wallet(user_id=user.id, balance=0)
        db.add(wallet)
        await db.commit()
        await db.refresh(wallet)

    return wallet

@router.post("/offline-credit")
async def request_offline_credit(
    payload: OfflineCreditRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    tx = WalletTransaction(
        user_id=user.id,
        amount=payload.amount,
        type=WalletTransactionType.OFFLINE_CREDIT,
        note=payload.note
    )
    db.add(tx)
    await db.commit()

    return {"message": "Offline credit request submitted", "status": "pending"}
