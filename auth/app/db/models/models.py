from typing import Optional
from uuid import uuid4
from sqlalchemy import (
    Computed,
    String,
    text,
    UniqueConstraint,
    func,
    UUID,
    ForeignKey,
    SMALLINT,
    Boolean,
    ARRAY,
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base
from sqlalchemy_utils import UUIDType


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[BYTEA] = mapped_column(type_=BYTEA(1024))
    surname: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    patronymic: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(10), server_default='user')
    is_archived: Mapped[bool] = mapped_column(Boolean, server_default='false')



class Role(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(12))
