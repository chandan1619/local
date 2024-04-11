"""initial migrations

Revision ID: c4a72e4196ac
Revises: 
Create Date: 2024-04-08 11:53:15.970427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4a72e4196ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_name', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_name', 'users', ['name'], unique=True)
    # ### end Alembic commands ###
