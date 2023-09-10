"""add users table

Revision ID: ffdfd3ee443b
Revises: 15632d06f03d
Create Date: 2023-09-10 12:42:57.772079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffdfd3ee443b'
down_revision: Union[str, None] = '15632d06f03d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
