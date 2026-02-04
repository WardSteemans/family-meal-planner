# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .models.database import init_db
from .routers import Users, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await init_db()
    yield
    # Shutdown (optional cleanup)

app = FastAPI(lifespan=lifespan)

app.include_router(Users.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Family Meal Planner API is running"}