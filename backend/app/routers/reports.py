from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.responses import StreamingResponse
import csv
import io
from datetime import datetime

from app.db import get_db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.service_request import ServiceRequest
from app.models.ledger import LedgerEntry
from app.models.audit_log import AuditLog
from app.core.security import require_admin

router = APIRouter(
    prefix="/admin/reports",
    tags=["Admin Reports"],
)


# -------------------------------------------------
# KPIs
# -------------------------------------------------
@router.get("/kpis", dependencies=[Depends(require_admin)])
def system_kpis(db: Session = Depends(get_db)):
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
        },
    }


# -------------------------------------------------
# Ledger Summary
# -------------------------------------------------
@router.get("/ledger", dependencies=[Depends(require_admin)])
def ledger_summary(
    db: Session = Depends(get_db),
    start_date: str | None = None,
    end_date: str | None = None,
):
    q = db.query(LedgerEntry)

    if start_date:
        q = q.filter(LedgerEntry.created_at >= start_date)
    if end_date:
        q = q.filter(LedgerEntry.created_at <= end_date)

    entries = q.order_by(LedgerEntry.created_at.desc()).all()

    return [
        {
            "id": e.id,
            "user_id": e.user_id,
            "wallet_id": e.wallet_id,
            "type": e.entry_type,
            "amount": float(e.amount),
            "currency": e.currency,
            "reference": e.reference,
            "admin_id": e.created_by_admin_id,
            "created_at": e.created_at,
        }
        for e in entries
    ]


# -------------------------------------------------
# Audit Log
# -------------------------------------------------
@router.get("/audit", dependencies=[Depends(require_admin)])
def audit_log(
    db: Session = Depends(get_db),
    start_date: str | None = None,
    end_date: str | None = None,
):
    q = db.query(AuditLog)

    if start_date:
        q = q.filter(AuditLog.created_at >= start_date)
    if end_date:
        q = q.filter(AuditLog.created_at <= end_date)

    logs = q.order_by(AuditLog.created_at.desc()).all()

    return [
        {
            "id": l.id,
            "admin_id": l.admin_id,
            "action": l.action,
            "target_type": l.target_type,
            "target_id": l.target_id,
            "description": l.description,
            "created_at": l.created_at,
        }
        for l in logs
    ]


# -------------------------------------------------
# CSV EXPORT — Ledger
# -------------------------------------------------
@router.get("/export/ledger", dependencies=[Depends(require_admin)])
def export_ledger_csv(db: Session = Depends(get_db)):
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "id",
        "user_id",
        "wallet_id",
        "type",
        "amount",
        "currency",
        "reference",
        "admin_id",
        "created_at",
    ])

    rows = db.query(LedgerEntry).order_by(LedgerEntry.created_at.desc()).all()
    for e in rows:
        writer.writerow([
            e.id,
            e.user_id,
            e.wallet_id,
            e.entry_type,
            float(e.amount),
            e.currency,
            e.reference,
            e.created_by_admin_id,
            e.created_at,
        ])

    output.seek(0)
    filename = f"ledger_export_{datetime.utcnow().isoformat()}.csv"

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# -------------------------------------------------
# CSV EXPORT — Audit Log
# -------------------------------------------------
@router.get("/export/audit", dependencies=[Depends(require_admin)])
def export_audit_csv(db: Session = Depends(get_db)):
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "id",
        "admin_id",
        "action",
        "target_type",
        "target_id",
        "description",
        "created_at",
    ])

    rows = db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
    for l in rows:
        writer.writerow([
            l.id,
            l.admin_id,
            l.action,
            l.target_type,
            l.target_id,
            l.description,
            l.created_at,
        ])

    output.seek(0)
    filename = f"audit_export_{datetime.utcnow().isoformat()}.csv"

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
