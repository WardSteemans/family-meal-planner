import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from .ingredient import GlobalIngredient
    # HIER ZAT DE FOUT: UserProfile zit in 'family', niet in 'user'
    from .family import UserProfile


class Recipe(SQLModel, table=True):
    __tablename__ = "recipes"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Verwijst naar de tabel 'user_profiles' die we in family.py hebben gemaakt
    created_by: uuid.UUID = Field(foreign_key="user_profiles.id")

    title: str = Field(index=True)
    description: Optional[str] = None
    steps: List[str] = Field(default=[], sa_column=Column(JSONB))

    servings: int
    prep_time_minutes: int
    nutritional_info: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    is_ai_generated: bool = Field(default=False)

    ingredients: List["RecipeIngredient"] = Relationship(back_populates="recipe",
                                                         sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class RecipeIngredient(SQLModel, table=True):
    __tablename__ = "recipe_ingredients"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    recipe_id: uuid.UUID = Field(foreign_key="recipes.id")
    global_ingredient_id: uuid.UUID = Field(foreign_key="global_ingredients.id")

    quantity: float
    unit: str
    note: Optional[str] = None

    recipe: Recipe = Relationship(back_populates="ingredients")

    # String referentie werkt het veiligst om imports te omzeilen
    global_ingredient: "GlobalIngredient" = Relationship()