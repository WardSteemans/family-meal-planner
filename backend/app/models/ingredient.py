from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # family_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("families.id"), nullable=False)
    # family: Mapped["Family"] = relationship("Family", back_populates="ingredients")
    family_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("families.id"),
        nullable=False,
    )

    family: Mapped["Family"] = relationship(
        "Family",
        back_populates="ingredients",
    )


    def __repr__(self):
        return f"Ingredient(id={self.id}, name={self.name}, family_id={self.family_id})"