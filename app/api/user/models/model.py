import uuid
from typing import Optional

from sqlalchemy import (
    UUID,
    Boolean,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.roles.models import Role
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[BYTEA] = mapped_column(type_=BYTEA(1024))
    surname: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    patronymic: Mapped[Optional[str]] = mapped_column(String(255))
    id_role: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, server_default="false")

    role: Mapped[Role] = relationship("Role", back_populates="users", lazy="noload")  # noqa: F821
