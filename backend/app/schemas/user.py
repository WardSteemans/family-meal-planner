# app/schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema with shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

# Schema for receiving data on POST /register
class UserCreate(UserBase):
    password: str

# Schema for returning data to client (sensitive info removed)
class UserOut(UserBase):
    id: UUID
    is_active: bool
    family_id: Optional[UUID] | None = None
    created_at: datetime

    # This config allows Pydantic to read data from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)