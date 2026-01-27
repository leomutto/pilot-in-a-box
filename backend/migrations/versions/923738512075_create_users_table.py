"""create users table

Revision ID: 923738512075
Revises: 1facca6dc8e8
Create Date: 2026-01-21 11:06:35.876046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from argon2 import PasswordHasher


# revision identifiers, used by Alembic.
revision: str = "923738512075"
down_revision: Union[str, Sequence[str], None] = "1facca6dc8e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Crear tabla users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # Crear usuario seed
    ph = PasswordHasher()
    hashed = ph.hash("Tremendo1#")

    # Alembic solo acepta SQL literal en op.execute()
    op.execute(
        f"INSERT INTO users (email, hashed_password) "
        f"VALUES ('ldmutto@gmail.com', '{hashed}')"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
