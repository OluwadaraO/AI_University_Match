"""add user authentication

Revision ID: 5c33f54a7955
Revises: c67700e74b59
Create Date: 2026-11-16 14:34:11.520027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c33f54a7955'
down_revision: Union[str, Sequence[str], None] = 'c67700e74b59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create user authentication tables and relationships."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True,
    )

    op.create_index(
        "ix_users_id",
        "users",
        ["id"],
        unique=False,
    )

    op.add_column(
        "students",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    op.create_unique_constraint(
        "uq_students_user_id",
        "students",
        ["user_id"],
    )

    op.create_foreign_key(
        "fk_students_user_id",
        "students",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    """Remove user authentication tables and relationships."""

    op.drop_constraint(
        "fk_students_user_id",
        "students",
        type_="foreignkey",
    )

    op.drop_constraint(
        "uq_students_user_id",
        "students",
        type_="unique",
    )

    op.drop_column(
        "students",
        "user_id",
    )

    op.drop_index(
        "ix_users_id",
        table_name="users",
    )

    op.drop_index(
        "ix_users_email",
        table_name="users",
    )

    op.drop_table("users")
