import uuid
from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .family import Family
    from .ingredient import GlobalIngredient


class InventoryItem(SQLModel, table=True):
    __tablename__ = "inventory_items"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    family_id: uuid.UUID = Field(foreign_key="families.id")

    # Nullable Foreign Key
    global_ingredient_id: Optional[uuid.UUID] = Field(default=None, foreign_key="global_ingredients.id")

    raw_name: str
    quantity_available: float
    unit: str
    expiration_date: Optional[date] = None
    location: str = Field(default="pantry")

    family: "Family" = Relationship(back_populates="inventory_items")
    global_ingredient: Optional["GlobalIngredient"] = Relationship()