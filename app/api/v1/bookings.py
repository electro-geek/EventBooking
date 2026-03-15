from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union
from app.db.session import get_db
from app.api import deps
from app.crud import crud
from app.schemas import schemas
from app.db.models import UserRole
from app.services import booking_service

router = APIRouter()

@router.post("/", response_model=Union[schemas.BookingOut, schemas.WaitlistOut])
async def book_ticket(
    booking_in: schemas.BookingCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.get_current_user)
):
    result, message = await booking_service.process_booking(
        db, booking_in, current_user.id, current_user.email, background_tasks
    )
    return result

@router.get("/my-bookings", response_model=List[schemas.BookingOut])
async def get_my_bookings(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.get_current_user)
):
    return await crud.get_user_bookings(db, current_user.id)
