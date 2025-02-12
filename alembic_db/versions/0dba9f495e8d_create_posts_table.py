"""create posts table

Revision ID: 0dba9f495e8d
Revises: 
Create Date: 2025-02-10 18:23:40.527495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dba9f495e8d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# handles the changes
# everytime you set an upgrade function, you have to set the downgrade fuction as well
def upgrade() -> None:
    # Create post table
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))
    pass

# handles rolling back any changes
def downgrade() -> None:
    op.drop_table('posts')
    pass
