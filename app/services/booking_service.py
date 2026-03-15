from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.db.models import Event, Booking, Waitlist, BookingStatus
from app.schemas.schemas import BookingCreate
from fastapi import HTTPException, status, BackgroundTasks
from app.tasks.background import send_booking_confirmation

async def process_booking(
    db: AsyncSession, 
    booking_in: BookingCreate, 
    user_id: int, 
    user_email: str,
    background_tasks: BackgroundTasks
):
    # Use SELECT ... FOR UPDATE for concurrency control
    result = await db.execute(
        select(Event).where(Event.id == booking_in.event_id).with_for_update()
    )
    event = result.scalars().first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.available_slots >= booking_in.ticket_quantity:
        # Sufficient slots available
        event.available_slots -= booking_in.ticket_quantity
        
        db_booking = Booking(
            user_id=user_id,
            event_id=booking_in.event_id,
            ticket_quantity=booking_in.ticket_quantity,
            status=BookingStatus.CONFIRMED
        )
        db.add(db_booking)
        await db.commit()
        await db.refresh(db_booking)
        
        # Trigger background task
        background_tasks.add_task(send_booking_confirmation, user_email, event.title)
        
        return db_booking, "Booking confirmed"
    else:
        # Add to waitlist
        db_waitlist = Waitlist(
            user_id=user_id,
            event_id=booking_in.event_id
        )
        db.add(db_waitlist)
        await db.commit()
        await db.refresh(db_waitlist)
        
        return db_waitlist, "Event full, added to waitlist"
