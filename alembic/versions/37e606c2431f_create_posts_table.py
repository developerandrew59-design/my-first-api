"""create posts table

Revision ID: 37e606c2431f
Revises: 
Create Date: 2026-02-26 21:55:39.763500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37e606c2431f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    #op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    #                sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
