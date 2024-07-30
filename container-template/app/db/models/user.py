import uuid
from sqlalchemy import (
    ForeignKey,
    String,
    UUID
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    store_id: Mapped[str] = mapped_column(ForeignKey("stores.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(server_default="false", nullable=False)
    sum: Mapped[float] = mapped_column(server_default="0")

    store: Mapped["Store"] = relationship(back_populates="user")

class Store(Base):
    __tablename__ = "stores"
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))

    user: Mapped[User] = relationship(back_populates="store")