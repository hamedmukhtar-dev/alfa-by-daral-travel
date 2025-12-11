from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import get_db
from ..models.wallet import Wallet
from ..models.user import User
from ..core.security import get_current_user

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/", summary="Get my wallet balance")
async def get_my_wallet(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Wallet).where(Wallet.user_id == current_user.id)
    )
    wallet = result.scalar_one_or_none()
    if wallet is None:
        wallet = Wallet(user_id=current_user.id, balance=0)
        db.add(wallet)
        await db.commit()
        await db.refresh(wallet)
    return {"balance": float(wallet.balance)}


@router.post("/credit", summary="Add credit to wallet (Test Mode)")
async def credit_wallet(
    amount: float,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    result = await db.execute(
        select(Wallet).where(Wallet.user_id == current_user.id)
    )
    wallet = result.scalar_one_or_none()
    if wallet is None:
        wallet = Wallet(user_id=current_user.id, balance=0)
        db.add(wallet)

    wallet.balance += amount
    await db.commit()
    await db.refresh(wallet)

    return {"status": "credited", "new_balance": float(wallet.balance)}


@router.post("/debit", summary="Deduct balance (Test Mode)")
async def debit_wallet(
    amount: float,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    result = await db.execute(
        select(Wallet).where(Wallet.user_id == current_user.id)
    )
    wallet = result.scalar_one_or_none()
    if wallet is None or wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    wallet.balance -= amount
    await db.commit()
    await db.refresh(wallet)

    return {"status": "debited", "new_balance": float(wallet.balance)}
