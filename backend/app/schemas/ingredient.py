from pydantic import BaseModel, ConfigDict
from uuid import UUID

class IngredientBase(BaseModel):
    name: str

class IngredientCreate(IngredientBase):
    pass

class IngredientOut(IngredientBase):
    id: UUID
    family_id: UUID

    model_config = ConfigDict(from_attributes=True)