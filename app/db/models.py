from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.session import Base

class UserRole(str, enum.Enum):
    ORGANIZER = "organizer"
    CUSTOMER = "customer"

class BookingStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)

    events = relationship("Event", back_populates="organizer")
    bookings = relationship("Booking", back_populates="user")
    waitlist_entries = relationship("Waitlist", back_populates="user")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    location = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_slots = Column(Integer, nullable=False)
    available_slots = Column(Integer, nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"))

    organizer = relationship("User", back_populates="events")
    bookings = relationship("Booking", back_populates="event")
    waitlist_entries = relationship("Waitlist", back_populates="event")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    booking_time = Column(DateTime, default=datetime.utcnow)
    status = Column(SQLAlchemyEnum(BookingStatus), default=BookingStatus.CONFIRMED)
    ticket_quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")

class Waitlist(Base):
    __tablename__ = "waitlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    priority_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="waitlist_entries")
    event = relationship("Event", back_populates="waitlist_entries")
