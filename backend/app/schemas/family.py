from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from typing import List, Optional
from .common import Role


# --- USER PROFILE ---
class UserProfileBase(BaseModel):
    name: str
    role: Role = Role.MEMBER
    preferences: List[str] = []
    allergies: List[str] = []
    avatar_url: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass  # Family ID wordt vaak uit de context/token gehaald


class UserProfile(UserProfileBase):
    id: UUID
    family_id: UUID
    model_config = ConfigDict(from_attributes=True)


# --- FAMILY ---
class FamilyBase(BaseModel):
    name: str
    budget_monthly: Optional[float] = None


class FamilyCreate(FamilyBase):
    pass


class Family(FamilyBase):
    id: UUID
    # We kunnen hier een lijst users nesten als we willen
    members: List[UserProfile] = []

    model_config = ConfigDict(from_attributes=True)