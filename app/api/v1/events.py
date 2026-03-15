from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.api import deps
from app.crud import crud
from app.schemas import schemas
from app.db.models import UserRole
from app.tasks.background import notify_event_update

router = APIRouter()

@router.get("/", response_model=List[schemas.EventOut])
async def list_events(db: AsyncSession = Depends(get_db)):
    return await crud.get_events(db)

@router.post("/", response_model=schemas.EventOut, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: schemas.EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.check_role(UserRole.ORGANIZER))
):
    return await crud.create_event(db, event_in, current_user.id)

@router.put("/{event_id}", response_model=schemas.EventOut)
async def update_event(
    event_id: int,
    event_in: schemas.EventUpdate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.check_role(UserRole.ORGANIZER))
):
    event = await crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not the organizer of this event")
    
    updated_event = await crud.update_event(db, event_id, event_in)
    
    # Background Task 2: Event Update Notification
    # Get all customers who booked for this event
    bookings = await crud.get_event_bookings(db, event_id)
    emails = [b.user.email for b in bookings]
    if emails:
        background_tasks.add_task(notify_event_update, emails, updated_event.title)
    
    return updated_event

@router.get("/{event_id}", response_model=schemas.EventOut)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
