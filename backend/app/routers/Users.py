# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserOut
from ..utils import password

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if user already exists (optional but recommended)
    query = select(User).where(User.email == user_in.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 2. Create new User model instance
    new_user = User(
        email=user_in.email,
        hashed_password=password.hash_password(user_in.password),
        name=user_in.name
    )

    # 3. Add to DB and commit
    db.add(new_user)
    await db.commit()

    # 4. Refresh to get the generated ID and created_at timestamp
    await db.refresh(new_user)

    return new_user