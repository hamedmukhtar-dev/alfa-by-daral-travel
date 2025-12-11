from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.auth import UserLogin, UserRegister, TokenResponse
from app.models.user import User
from app.core.hashing import verify_password, hash_password
from app.core.security import create_access_token, get_current_user
from sqlalchemy.future import select


router = APIRouter(prefix="/auth", tags=["Authentication"])


# -------------------------------
# REGISTER
# -------------------------------
@router.post("/register", response_model=TokenResponse)
async def register_user(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == payload.email))
    existing = result.scalars().first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_active=True,
        is_admin=False,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Issue token
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, user_id=user.id)


# -------------------------------
# LOGIN
# -------------------------------
@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalars().first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, user_id=user.id)


# -------------------------------
# VALIDATE TOKEN
# -------------------------------
@router.get("/validate", response_model=TokenResponse)
async def validate_token(current_user: User = Depends(get_current_user)):
    token = create_access_token({"sub": str(current_user.id)})
    return TokenResponse(access_token=token, user_id=current_user.id)


# -------------------------------
# LOGOUT (client-side)
# -------------------------------
@router.post("/logout")
async def logout():
    return {"detail": "Logout successful. Remove token client-side."}
