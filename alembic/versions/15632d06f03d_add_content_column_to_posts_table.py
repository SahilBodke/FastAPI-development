"""add content column to posts table

Revision ID: 15632d06f03d
Revises: 12d3e9d3dc0b
Create Date: 2023-09-10 12:38:08.091160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15632d06f03d'
down_revision: Union[str, None] = '12d3e9d3dc0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
