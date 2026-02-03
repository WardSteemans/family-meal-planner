from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from .common import IngredientCategory


# --- GLOBAL INGREDIENT ---
class GlobalIngredientBase(BaseModel):
    name: str
    default_unit: str = "stuks"
    category: IngredientCategory = IngredientCategory.OTHER
    nutritional_per_100g: Optional[dict] = None


class GlobalIngredientCreate(GlobalIngredientBase):
    pass


class GlobalIngredient(GlobalIngredientBase):
    id: UUID

    # Dit zorgt ervoor dat Pydantic data uit je SQLAlchemy database snapt
    model_config = ConfigDict(from_attributes=True)