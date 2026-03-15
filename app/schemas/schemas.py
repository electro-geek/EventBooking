from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from app.db.models import UserRole, BookingStatus

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None

# Event Schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    total_slots: int

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_slots: Optional[int] = None

class EventOut(EventBase):
    id: int
    available_slots: int
    organizer_id: int

    class Config:
        from_attributes = True

# Booking Schemas
class BookingBase(BaseModel):
    event_id: int
    ticket_quantity: int = 1

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    user_id: int
    booking_time: datetime
    status: BookingStatus

    class Config:
        from_attributes = True

# Waitlist Schemas
class WaitlistOut(BaseModel):
    id: int
    user_id: int
    event_id: int
    priority_score: int
    created_at: datetime

    class Config:
        from_attributes = True
