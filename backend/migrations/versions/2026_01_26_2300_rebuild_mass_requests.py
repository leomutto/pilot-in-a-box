"""Rebuild mass_requests table aligned with MASS Simple v1.0 / Enterprise v1.1

Revision ID: rebuild_mass_requests_20260126
Revises: 923738512075
Create Date: 2026-01-26 23:00:00
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "rebuild_mass_requests_20260126"
down_revision: Union[str, Sequence[str], None] = "923738512075"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop old table and create new MASS Simple v1.0 table."""

    # Drop old table if exists
    op.drop_table("mass_requests")

    # Create new table aligned with MassRequest model
    op.create_table(
        "mass_requests",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("schema_version", sa.String, nullable=False),
        sa.Column("correlation_id", sa.String, nullable=False),
        sa.Column("idempotency_key", sa.String, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("payload_json", sa.JSON, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    # Explicit indexes (sin index=True en las columnas)
    op.create_index(
        "ix_mass_requests_correlation_id",
        "mass_requests",
        ["correlation_id"],
    )
    op.create_index(
        "ix_mass_requests_idempotency_key",
        "mass_requests",
        ["idempotency_key"],
    )


def downgrade() -> None:
    """Rollback: drop new table and recreate minimal old version."""

    op.drop_index("ix_mass_requests_correlation_id", table_name="mass_requests")
    op.drop_index("ix_mass_requests_idempotency_key", table_name="mass_requests")
    op.drop_table("mass_requests")

    # Recreate old minimal table (for rollback compatibility)
    op.create_table(
        "mass_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
