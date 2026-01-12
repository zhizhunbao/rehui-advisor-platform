from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    user_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AnonymousSessionResponse(BaseModel):
    session_token: str
    user_id: str
    user_type: str
    search_limit: int
    search_count: int


class QuotaStatusResponse(BaseModel):
    user_type: str
    search_count: int
    search_limit: int
    remaining: int
    quota_reset_at: str | None = None


class UserResponse(BaseModel):
    id: str
    email: str | None
    name: str | None
    user_type: str
    is_anonymous: bool
    search_limit: int
    search_count: int

    class Config:
        from_attributes = True
