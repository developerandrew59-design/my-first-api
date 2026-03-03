"""add foreign-key to posts table

Revision ID: bcf3d63d11b2
Revises: efa0195b8c3e
Create Date: 2026-02-27 14:55:21.836319

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcf3d63d11b2'
down_revision: Union[str, Sequence[str], None] = 'efa0195b8c3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('account_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_account_fkey',source_table="posts",referent_table="account",
    local_cols=['account_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_account_fkey',table_name='posts')
    op.drop_column('posts','account_id')
    pass
