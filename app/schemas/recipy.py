from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, Optional
from .ingredient import GlobalIngredient


# --- RECIPE INGREDIENT (De koppeling in een recept) ---
class RecipeIngredientBase(BaseModel):
    quantity: float
    unit: str
    note: Optional[str] = None  # bijv. "fijngesneden"

    # We verwachten bij het maken alleen een ID
    global_ingredient_id: UUID


class RecipeIngredientResponse(RecipeIngredientBase):
    id: UUID
    # Nesten: laat de details van het global ingredient zien
    global_ingredient: Optional[GlobalIngredient] = None

    model_config = ConfigDict(from_attributes=True)


# --- RECIPE ---
class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    steps: List[str] = []
    servings: int
    prep_time_minutes: int
    nutritional_info: Optional[dict] = None


class RecipeCreate(RecipeBase):
    # Bij aanmaken sturen we een lijst ingrediënten mee
    ingredients: List[RecipeIngredientBase]


class Recipe(RecipeBase):
    id: UUID
    is_ai_generated: bool
    created_by: UUID
    ingredients: List[RecipeIngredientResponse] = []

    model_config = ConfigDict(from_attributes=True)