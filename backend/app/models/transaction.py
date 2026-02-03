import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from .family import Family, UserProfile


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Foreign Keys
    family_id: uuid.UUID = Field(foreign_key="families.id")
    payer_id: uuid.UUID = Field(foreign_key="user_profiles.id")

    transaction_date: datetime = Field(default_factory=datetime.utcnow)
    total_amount: float
    image_url: Optional[str] = None

    # JSONB veld (voor de gescande items)
    # Let op: sa_column is nodig voor JSONB in SQLModel
    parsed_items: List[dict] = Field(default=[], sa_column=Column(JSONB))

    # Relaties
    family: "Family" = Relationship(back_populates="transactions")
    payer: "UserProfile" = Relationship()