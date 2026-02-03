import uuid
from datetime import date
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from schemas.common import MealType

if TYPE_CHECKING:
    from .family import Family, UserProfile
    from .recipy import Recipe


# KOPPELTABEL (Join Table)
class MealPlanAssignment(SQLModel, table=True):
    __tablename__ = "meal_plan_assignments"

    meal_plan_id: uuid.UUID = Field(foreign_key="meal_plans.id", primary_key=True)
    user_profile_id: uuid.UUID = Field(foreign_key="user_profiles.id", primary_key=True)


class MealPlan(SQLModel, table=True):
    __tablename__ = "meal_plans"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    family_id: uuid.UUID = Field(foreign_key="families.id")
    recipe_id: uuid.UUID = Field(foreign_key="recipes.id")

    date: date
    # Enum werkt direct in SQLModel als je het type hint
    meal_type: MealType
    notes: Optional[str] = None

    # Relaties
    family: "Family" = Relationship(back_populates="meal_plans")
    recipe: "Recipe" = Relationship()

    # Many-to-Many relatie via de koppeltabel
    assigned_users: List["UserProfile"] = Relationship(link_model=MealPlanAssignment)