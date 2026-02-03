import uuid
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

from ..schemas.common import IngredientCategory

class GlobalIngredient(SQLModel, table=True):
    __tablename__ = "global_ingredients"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    default_unit: str = Field(default="stuks")

    category: IngredientCategory = Field(default=IngredientCategory.OTHER)

    nutritional_per_100g: Optional[dict] = Field(default=None, sa_column=Column(JSONB))