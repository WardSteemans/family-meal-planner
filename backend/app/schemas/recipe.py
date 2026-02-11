from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeOut(RecipeBase):
    id: UUID
    family_id: UUID

    model_config = ConfigDict(from_attributes=True)