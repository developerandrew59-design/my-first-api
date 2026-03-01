"""add content to posts table

Revision ID: 6dc9971e50ad
Revises: 37e606c2431f
Create Date: 2026-02-27 11:29:18.771478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dc9971e50ad'
down_revision: Union[str, Sequence[str], None] = '37e606c2431f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
