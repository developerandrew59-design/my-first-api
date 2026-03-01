"""add account table

Revision ID: efa0195b8c3e
Revises: 6dc9971e50ad
Create Date: 2026-02-27 11:36:43.237951

"""
from time import timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efa0195b8c3e'
down_revision: Union[str, Sequence[str], None] = '6dc9971e50ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('account',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),
                              nullable=False),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('account')
    pass
