import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Column, String



from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Family(Base):
    __tablename__ = "families"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    #relationship to access family.users
    users: Mapped[List["User"]] = relationship("User", back_populates="family")


    def __repr__(self):
        return f"Family(id={self.id}, name={self.name})"