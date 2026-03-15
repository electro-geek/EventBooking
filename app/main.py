from fastapi import FastAPI
from app.api.v1 import auth, events, bookings
from app.db.session import engine, Base
import uvicorn

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if they don't exist (Runs on startup)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown logic (if any) here

app = FastAPI(
    title="Event Booking System",
    description="Backend for managing events and ticket bookings",
    version="1.0.0",
    lifespan=lifespan
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Event Booking System API"}

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
