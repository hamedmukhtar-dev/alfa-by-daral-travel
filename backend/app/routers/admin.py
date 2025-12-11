from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_db
from app.models.user import User
from app.models.service_request import ServiceRequest
from app.schemas.admin import AdminUpdate, AdminResponse
from app.core.security import get_current_user


router = APIRouter(prefix="/admin", tags=["Admin Panel"])


# -------------------------------
# SUPERADMIN CHECK
# -------------------------------
async def require_superadmin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied — SuperAdmin only",
        )
    return current_user


# -------------------------------
# GET ALL USERS
# -------------------------------
@router.get("/users", response_model=list[AdminResponse])
async def list_all_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_superadmin),
):
    result = await db.execute(select(User))
    return result.scalars().all()


# -------------------------------
# UPDATE USER BY ADMIN
# -------------------------------
@router.put("/users/{user_id}", response_model=AdminResponse)
async def update_user_by_admin(
    user_id: int,
    data: AdminUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_superadmin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(404, "User not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


# -------------------------------
# DELETE USER
# -------------------------------
@router.delete("/users/{user_id}")
async def delete_user_by_admin(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_superadmin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(404, "User not found")

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted successfully"}


# -------------------------------
# VIEW ALL SERVICE REQUESTS
# -------------------------------
@router.get("/requests")
async def list_service_requests(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_superadmin),
):
    result = await db.execute(select(ServiceRequest))
    return result.scalars().all()


# -------------------------------
# ADMIN OVERVIEW
# -------------------------------
@router.get("/overview")
async def admin_overview(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_superadmin),
):
    total_users = await db.execute(select(User))
    total_requests = await db.execute(select(ServiceRequest))

    return {
        "total_users": len(total_users.scalars().all()),
        "total_requests": len(total_requests.scalars().all()),
        "message": "Welcome SuperAdmin — ALFA Control Center",
    }
