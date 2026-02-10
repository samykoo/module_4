from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """회원가입 요청 스키마"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class UserResponse(BaseModel):
    """API 응답 스키마 (비밀번호 제외)"""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserInDB(BaseModel):
    """내부 로직용 스키마 (모든 필드 포함)"""
    id: int
    username: str
    email: str
    hashed_password: str
    created_at: datetime

    class Config:
        from_attributes = True
