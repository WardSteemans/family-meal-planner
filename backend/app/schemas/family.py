from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class FamilyBase(BaseModel):
    name: str

class FamilyCreate(FamilyBase):
    pass

class FamilyOut(FamilyBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FamilyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)