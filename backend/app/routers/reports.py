from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.service_request import ServiceRequest
from app.core.security import require_admin

router = APIRouter(
    prefix="/admin/reports",
    tags=["Admin Reports"],
)

# ---------------------------
# SYSTEM KPIs
# ---------------------------
@router.get("/kpis", dependencies=[Depends(require_admin)])
def get_system_kpis(db: Session = Depends(get_db)):
    return {
        "users": {
            "total": db.query(func.count(User.id)).scalar(),
            "active": db.query(func.count(User.id)).filter(User.is_active == True).scalar(),
        },
        "wallets": {
            "total_balance": float(db.query(func.coalesce(func.sum(Wallet.balance), 0)).scalar()),
            "pending_credit": float(db.query(func.coalesce(func.sum(Wallet.pending_amount), 0)).scalar()),
        },
        "service_requests": {
            "total": db.query(func.count(ServiceRequest.id)).scalar(),
            "pending": db.query(func.count(ServiceRequest.id))
                .filter(ServiceRequest.status == "pending")
                .scalar(),
        }
    }


# ---------------------------
# WALLET REPORT
# ---------------------------
@router.get("/wallets", dependencies=[Depends(require_admin)])
def wallet_report(db: Session = Depends(get_db)):
    wallets = db.query(Wallet).all()
    return [
        {
            "user_id": w.user_id,
            "balance": float(w.balance),
            "pending_amount": float(w.pending_amount),
            "updated_at": w.updated_at,
        }
        for w in wallets
    ]


# ---------------------------
# SERVICE REQUESTS REPORT
# ---------------------------
@router.get("/service-requests", dependencies=[Depends(require_admin)])
def service_requests_report(db: Session = Depends(get_db)):
    data = (
        db.query(
            ServiceRequest.service_type,
            ServiceRequest.status,
            func.count(ServiceRequest.id)
        )
        .group_by(ServiceRequest.service_type, ServiceRequest.status)
        .all()
    )

    report = {}
    for service_type, status, count in data:
        report.setdefault(service_type, {})
        report[service_type][status] = count

    return report
