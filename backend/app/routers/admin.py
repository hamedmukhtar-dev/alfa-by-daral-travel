from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db import get_db
from app.models.user import User
from app.models.service_request import ServiceRequest
from app.models.offline_payment import OfflinePayment

from app.core.security import get_current_user, require_admin
from app.core.audit import log_admin_action

router = APIRouter(prefix="/admin", tags=["Admin"])


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def _ensure_pending(entity, entity_name: str):
    if getattr(entity, "status", None) != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"{entity_name} already processed",
        )


# -------------------------------------------------
# Service Requests — Approve
# -------------------------------------------------
@router.post("/service-requests/approve", dependencies=[Depends(require_admin)])
def approve_service_request(
    payload: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_user),
):
    """
    payload = {
        "request_id": 123,
        "note": "approved for processing"
    }
    """
    request_id = payload.get("request_id")
    note = payload.get("note")

    if request_id is None:
        raise HTTPException(status_code=400, detail="request_id is required")

    req = db.query(ServiceRequest).filter(ServiceRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Service request not found")

    _ensure_pending(req, "Service request")

    req.status = "approved"
    db.add(req)
    db.commit()
    db.refresh(req)

    log_admin_action(
        db,
        admin_id=admin_user.id,
        action="approve_service_request",
        target_type="service_request",
        target_id=req.id,
        description=note or "Service request approved",
    )

    return {
        "message": "Service request approved",
        "request_id": req.id,
        "status": req.status,
    }


# -------------------------------------------------
# Service Requests — Reject
# -------------------------------------------------
@router.post("/service-requests/reject", dependencies=[Depends(require_admin)])
def reject_service_request(
    payload: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_user),
):
    """
    payload = {
        "request_id": 123,
        "reason": "invalid data"
    }
    """
    request_id = payload.get("request_id")
    reason = payload.get("reason")

    if request_id is None:
        raise HTTPException(status_code=400, detail="request_id is required")

    req = db.query(ServiceRequest).filter(ServiceRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Service request not found")

    _ensure_pending(req, "Service request")

    req.status = "rejected"
    db.add(req)
    db.commit()
    db.refresh(req)

    log_admin_action(
        db,
        admin_id=admin_user.id,
        action="reject_service_request",
        target_type="service_request",
        target_id=req.id,
        description=reason or "Service request rejected",
    )

    return {
        "message": "Service request rejected",
        "request_id": req.id,
        "status": req.status,
    }


# -------------------------------------------------
# Offline Payments — List (Admin View)
# -------------------------------------------------
@router.get("/offline-payments", dependencies=[Depends(require_admin)])
def list_offline_payments(
    db: Session = Depends(get_db),
):
    payments = db.query(OfflinePayment).order_by(OfflinePayment.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "amount": float(p.amount),
            "method": p.method,
            "status": p.status,
            "reference": p.reference,
            "created_at": p.created_at,
        }
        for p in payments
    ]


# -------------------------------------------------
# Admin Safety — Double Action Guard
# -------------------------------------------------
@router.post("/guard/check-pending", dependencies=[Depends(require_admin)])
def check_pending_guard(
    payload: dict,
    db: Session = Depends(get_db),
):
    """
    Generic guard endpoint to verify entity is still pending
    payload = {
        "entity": "service_request" | "offline_payment",
        "entity_id": 123
    }
    """
    entity = payload.get("entity")
    entity_id = payload.get("entity_id")

    if entity not in {"service_request", "offline_payment"}:
        raise HTTPException(status_code=400, detail="invalid entity type")

    if entity_id is None:
        raise HTTPExcepti
