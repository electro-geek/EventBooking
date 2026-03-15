from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.db.models import User, Event, Booking, Waitlist, UserRole, BookingStatus
from app.schemas.schemas import UserCreate, EventCreate, EventUpdate, BookingCreate
from app.core.security import get_password_hash

# User CRUD
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate):
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Event CRUD
async def create_event(db: AsyncSession, event_in: EventCreate, organizer_id: int):
    db_event = Event(
        **event_in.dict(),
        available_slots=event_in.total_slots,
        organizer_id=organizer_id
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event

async def get_events(db: AsyncSession):
    result = await db.execute(select(Event))
    return result.scalars().all()

async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(Event).where(Event.id == event_id))
    return result.scalars().first()

async def update_event(db: AsyncSession, event_id: int, event_in: EventUpdate):
    db_event = await get_event(db, event_id)
    if not db_event:
        return None
    
    update_data = event_in.dict(exclude_unset=True)
    
    # If total_slots is updated, we need to adjust available_slots carefully
    if "total_slots" in update_data:
        diff = update_data["total_slots"] - db_event.total_slots
        db_event.available_slots += diff
        if db_event.available_slots < 0:
            # This is a bit tricky, might need validation earlier. 
            # For now, just allow it or cap at 0
            db_event.available_slots = 0

    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    await db.commit()
    await db.refresh(db_event)
    return db_event

# Booking CRUD
async def create_booking(db: AsyncSession, booking_in: BookingCreate, user_id: int):
    # This should be handled in a service layer for transaction control
    # But for simple CRUD:
    db_booking = Booking(
        user_id=user_id,
        event_id=booking_in.event_id,
        ticket_quantity=booking_in.ticket_quantity
    )
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking

async def get_user_bookings(db: AsyncSession, user_id: int):
    result = await db.execute(select(Booking).where(Booking.user_id == user_id))
    return result.scalars().all()

async def get_event_bookings(db: AsyncSession, event_id: int):
    result = await db.execute(select(Booking).where(Booking.event_id == event_id))
    return result.scalars().all()
