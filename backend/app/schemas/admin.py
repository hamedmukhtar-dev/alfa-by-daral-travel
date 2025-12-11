from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class AdminBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_superadmin: bool = False


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superadmin: Optional[bool] = None


class AdminResponse(AdminBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_id: int
