"""initial schema

Revision ID: 20260510_01
Revises:
Create Date: 2026-05-10 00:00:00
"""

from alembic import op

from app.models import Base

# revision identifiers, used by Alembic.
revision = "20260510_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind)
