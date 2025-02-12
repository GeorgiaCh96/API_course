"""add content column to posts table

Revision ID: 8c66a8531eec
Revises: 0dba9f495e8d
Create Date: 2025-02-10 18:36:26.219869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c66a8531eec'
down_revision: Union[str, None] = '0dba9f495e8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
