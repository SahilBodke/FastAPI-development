"""create posts table

Revision ID: 12d3e9d3dc0b
Revises: 
Create Date: 2023-09-10 00:47:11.871501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12d3e9d3dc0b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:  # To make modifications
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True), 
                             sa.Column('title', sa.String(), nullable = False))
    


def downgrade() -> None:  # To rollback
    op.drop_table('posts')
