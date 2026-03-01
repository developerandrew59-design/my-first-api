"""add few last coloumns you missed in posts table

Revision ID: 165c117ed1af
Revises: bcf3d63d11b2
Create Date: 2026-02-27 15:41:55.896035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '165c117ed1af'
down_revision: Union[str, Sequence[str], None] = 'bcf3d63d11b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),
                  )
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,
                                    server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
