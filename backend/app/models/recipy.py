import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    family_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("families.id"), nullable=False)
    family: Mapped["Family"] = relationship("Family", back_populates="recipes")

    def __repr__(self):
        return f"Recipe(id={self.id}, title={self.title}, family_id={self.family_id})"