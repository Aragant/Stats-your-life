"""add date for the routine

Revision ID: 89e23cff65b5
Revises: 742061e4427e
Create Date: 2025-09-28 22:20:45.939779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "89e23cff65b5"
down_revision: Union[str, Sequence[str], None] = "742061e4427e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. ajouter la colonne en nullable
    op.add_column("session", sa.Column("date", sa.String(), nullable=True))

    # 2. remplir les anciennes lignes avec une valeur
    op.execute("UPDATE session SET date = CURRENT_DATE")

    # 3. rendre la colonne NOT NULL
    op.alter_column("session", "date", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("session", "date")
