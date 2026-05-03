from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):

    name: str
    email: EmailStr


class UserCreate(UserBase):

    password: str


class UserUpdate(BaseModel):

    id: int

    status: str


class UserBooking(BaseModel):
    father_name: str
    section: str
    semester: int
    roll_no: str


class UserResponse(UserBase):
    id: int
    father_name: Optional[str]
    section: Optional[str]
    semester: Optional[int]
    roll_no: Optional[str]
    status: Optional[str]
    is_ticket_used: Optional[bool]
    is_applied: Optional[bool]
    created_at: Optional[datetime]
    entered_time: Optional[datetime]

    class Config:
        from_attributes = True


class Token(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None
