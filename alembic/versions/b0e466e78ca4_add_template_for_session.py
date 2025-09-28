"""add template for session

Revision ID: b0e466e78ca4
Revises: 89e23cff65b5
Create Date: 2025-09-28 23:35:55.387682
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0e466e78ca4'
down_revision: Union[str, Sequence[str], None] = '89e23cff65b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Ajouter la colonne nullable
    op.add_column("session", sa.Column("template", sa.Boolean(), nullable=True))

    # 2. Remplir les anciennes lignes avec False
    op.execute("UPDATE session SET template = FALSE")

    # 3. Passer la colonne en NOT NULL
    op.alter_column("session", "template", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("session", "template")
