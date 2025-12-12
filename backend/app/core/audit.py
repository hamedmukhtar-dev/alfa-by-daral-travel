from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


def log_admin_action(
    db: Session,
    *,
    admin_id: int,
    action: str,
    target_type: str,
    target_id: int | None = None,
    description: str | None = None,
):
    log = AuditLog(
        admin_id=admin_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        description=description,
    )
    db.add(log)
    db.commit()
