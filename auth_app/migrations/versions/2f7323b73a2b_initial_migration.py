"""Initial migration

Revision ID: 2f7323b73a2b
Revises: 
Create Date: 2024-11-26 11:09:48.844328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '2f7323b73a2b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('widgets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.String(), nullable=True),
    sa.Column('secret_key', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subdomain', sa.String(), nullable=True),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('unactive_reason', sa.String(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('widget_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['widget_id'], ['widgets.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('subdomain')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    op.drop_table('widgets')
