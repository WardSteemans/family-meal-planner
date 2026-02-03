from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date
from typing import Optional
from .ingredient import GlobalIngredient


class InventoryItemBase(BaseModel):
    quantity_available: float
    unit: str
    expiration_date: Optional[date] = None
    location: str = "pantry"

    # De keuze: Of een ID, of een raw_name (of beide)
    global_ingredient_id: Optional[UUID] = None
    raw_name: Optional[str] = None


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItem(InventoryItemBase):
    id: UUID
    family_id: UUID
    # Als er een match is, toon de details
    global_ingredient: Optional[GlobalIngredient] = None

    model_config = ConfigDict(from_attributes=True)