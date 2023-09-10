"""add foreign key to posts table

Revision ID: 889c3e5ce68a
Revises: 82c0a7405044
Create Date: 2023-09-10 14:35:51.750982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '889c3e5ce68a'
down_revision: Union[str, None] = '82c0a7405044'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")   # Set relation between posts and users
 

def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column("posts", "owner_id")
    
