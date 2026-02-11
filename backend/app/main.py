# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .models.database import init_db
from .routers import Users, auth, families, ingredients, recipes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await init_db()
    yield
    # Shutdown (optional cleanup)

app = FastAPI(lifespan=lifespan)

app.include_router(Users.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(families.router, prefix="/api/v1/families", tags=["families"])
app.include_router(ingredients.router, prefix="/api/v1", tags=["ingredients"])
app.include_router(recipes.router, prefix="/api/v1", tags=["recipes"])

@app.get("/")
def read_root():
    return {"message": "Family Meal Planner API is running"}