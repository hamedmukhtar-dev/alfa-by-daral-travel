from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models.wallet import Wallet, WalletTransaction, WalletTransactionStatus
from app.core.security import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/wallet/pending")
async def list_pending_wallet_requests(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    result = await db.execute(
        select(WalletTransaction).where(WalletTransaction.status == WalletTransactionStatus.PENDING)
    )
    return result.scalars().all()

@router.post("/wallet/{tx_id}/approve")
async def approve_wallet_request(
    tx_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    result = await db.execute(select(WalletTransaction).where(WalletTransaction.id == tx_id))
    tx = result.scalar_one_or_none()

    if not tx or tx.status != WalletTransactionStatus.PENDING:
        raise HTTPException(status_code=404, detail="Transaction not found")

    wallet_result = await db.execute(select(Wallet).where(Wallet.user_id == tx.user_id))
    wallet = wallet_result.scalar_one_or_none()

    if not wallet:
        wallet = Wallet(user_id=tx.user_id, balance=0)
        db.add(wallet)

    wallet.balance += tx.amount
    tx.status = WalletTransactionStatus.APPROVED

    await db.commit()
    return {"message": "Approved", "balance": wallet.balance}

@router.post("/wallet/{tx_id}/reject")
async def reject_wallet_request(
    tx_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    result = await db.execute(select(WalletTransaction).where(WalletTransaction.id == tx_id))
    tx = result.scalar_one_or_none()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    tx.status = WalletTransactionStatus.REJECTED
    await db.commit()

    return {"message": "Rejected"}
