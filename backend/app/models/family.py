import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB

from ..schemas.common import Role

if TYPE_CHECKING:
    from .inventory import InventoryItem
    from .meal_plan import MealPlan
    from .recipy import Recipe
    from .transaction import Transaction


class Family(SQLModel, table=True):
    __tablename__ = "families"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    budget_monthly: Optional[float] = None

    members: List["UserProfile"] = Relationship(back_populates="family",
                                                sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    inventory_items: List["InventoryItem"] = Relationship(back_populates="family")
    meal_plans: List["MealPlan"] = Relationship(back_populates="family")
    transactions: List["Transaction"] = Relationship(back_populates="family")


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    family_id: uuid.UUID = Field(foreign_key="families.id")

    name: str
    role: Role = Field(default=Role.MEMBER)
    avatar_url: Optional[str] = None

    preferences: List[str] = Field(default=[], sa_column=Column(JSONB))
    allergies: List[str] = Field(default=[], sa_column=Column(JSONB))

    family: Family = Relationship(back_populates="members")