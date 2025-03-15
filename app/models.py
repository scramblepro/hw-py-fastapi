import datetime
import uuid
from sqlalchemy import (
    UUID, Boolean, Column, DateTime, ForeignKey, String, Table, UniqueConstraint, func, Text
)
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, SQL_DEBUG

engine = create_async_engine(
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
    echo=SQL_DEBUG,
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass

role_rights = Table(
    "role_right_relation", Base.metadata,
    Column("role_id", ForeignKey("role.id"), index=True),
    Column("right_id", ForeignKey("right.id"), index=True),
)

user_roles = Table(
    "user_role_relation", Base.metadata,
    Column("user_id", ForeignKey("todo_user.id"), index=True),
    Column("role_id", ForeignKey("role.id"), index=True),
)

class Right(Base):
    __tablename__ = "right"
    __table_args__ = (
        UniqueConstraint("model", "write", "read", "only_own"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    write: Mapped[bool] = mapped_column(Boolean, default=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    only_own: Mapped[bool] = mapped_column(Boolean, default=True)
    model: Mapped[str] = mapped_column(String(50), nullable=False)

class Role(Base):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    rights: Mapped[list[Right]] = relationship(secondary=role_rights, lazy="joined")

class User(Base):
    __tablename__ = "todo_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    tokens: Mapped[list["Token"]] = relationship("Token", back_populates="user", cascade="all, delete-orphan", lazy="joined")
    roles: Mapped[list[Role]] = relationship(secondary=user_roles, lazy="joined")

class Token(Base):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, server_default=func.gen_random_uuid(), unique=True)
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("todo_user.id"))
    user: Mapped[User] = relationship(User, back_populates="tokens", lazy="joined")

class Advertisement(Base):
    __tablename__ = "advertisement"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    author_id: Mapped[int] = mapped_column(ForeignKey("todo_user.id"), nullable=False)
    author: Mapped[User] = relationship(User, back_populates="advertisements")

User.advertisements = relationship("Advertisement", back_populates="author", cascade="all, delete-orphan", lazy="joined")