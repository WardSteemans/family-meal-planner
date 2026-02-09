from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
import uuid
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.database import get_db
from ..models.user import User

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 1. Define OAuth2 Scheme pointing to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 2. Create reusable dependency
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 3. Decode and validate token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 4. Fetch user from database
    try:
        # Cast user_id string to UUID for the query
        query = select(User).where(User.id == uuid.UUID(user_id))
        result = await db.execute(query)
        user = result.scalar_one_or_none()
    except (ValueError, TypeError):
        # Handle cases where the ID in the token is not a valid UUID
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return user