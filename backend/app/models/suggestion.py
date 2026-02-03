import uuid
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from .family import UserProfile


class GeneratedSuggestion(SQLModel, table=True):
    __tablename__ = "generated_suggestions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_profile_id: uuid.UUID = Field(foreign_key="user_profiles.id")

    prompt: str
    based_on_inventory: bool = Field(default=False)

    # JSON veld voor het gegenereerde recept
    generated_recipe_json: dict = Field(default={}, sa_column=Column(JSONB))

    user_profile: "UserProfile" = Relationship()