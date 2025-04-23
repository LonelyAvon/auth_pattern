import uuid
from typing import List

from sqlalchemy import (
    UUID,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    users: Mapped[List["User"]] = relationship("User", back_populates="role")  # noqa: F821
