import os
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import scripts

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

# revision identifiers, used by Alembic.
revision: str = "a2081e7ef2b4"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


async def create_admin_user(session: AsyncSession, username: str, password: str) -> None:
    await scripts.create_admin_user(session, username, password)


async def create_user_role(session: AsyncSession) -> None:
    await scripts.create_user_role(session)


def upgrade() -> None:
    op.create_table(
        "right",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("write", sa.Boolean(), nullable=False),
        sa.Column("read", sa.Boolean(), nullable=False),
        sa.Column("only_own", sa.Boolean(), nullable=False),
        sa.Column("model", sa.String(length=50), nullable=False),
        sa.CheckConstraint("model in ('user', 'todo', 'token', 'role', 'right')"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("model", "write", "read", "only_own"),
    )
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "todo_user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=70), nullable=False),
        sa.Column(
            "registration_time",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "role_right_relation",
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column("right_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["right_id"], ["right.id"]),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"]),
    )
    op.create_index(
        op.f("ix_role_right_relation_right_id"),
        "role_right_relation",
        ["right_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_role_right_relation_role_id"),
        "role_right_relation",
        ["role_id"],
        unique=False,
    )
    op.create_table(
        "todo",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("important", sa.Boolean(), nullable=False),
        sa.Column("done", sa.Boolean(), nullable=False),
        sa.Column(
            "start_time",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("finish_time", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["todo_user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "token",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "token",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "creation_time",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["todo_user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_table(
        "user_role_relation",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["todo_user.id"]),
    )
    op.create_index(
        op.f("ix_user_role_relation_role_id"),
        "user_role_relation",
        ["role_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_role_relation_user_id"),
        "user_role_relation",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_user_role_relation_user_id"), table_name="user_role_relation")
    op.drop_index(op.f("ix_user_role_relation_role_id"), table_name="user_role_relation")
    op.drop_table("user_role_relation")
    op.drop_table("token")
    op.drop_table("todo")
    op.drop_index(op.f("ix_role_right_relation_role_id"), table_name="role_right_relation")
    op.drop_index(op.f("ix_role_right_relation_right_id"), table_name="role_right_relation")
    op.drop_table("role_right_relation")
    op.drop_table("todo_user")
    op.drop_table("role")
    op.drop_table("right")
