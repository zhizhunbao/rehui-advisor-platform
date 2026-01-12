"""管理员认证 DTO"""
from pydantic import BaseModel, EmailStr


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    token: str
    admin: dict


class CreateAdminRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    role: str


class UpdateAdminPasswordRequest(BaseModel):
    old_password: str
    new_password: str


class AdminResponse(BaseModel):
    id: str
    username: str
    email: str
    name: str
    role: str
    is_active: bool
    last_login_at: str

    class Config:
        from_attributes = True
