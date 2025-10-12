"""add order confirmation column

Revision ID: add_order_confirmation_column
Create Date: 2025-10-13
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('order', sa.Column('confirmed', sa.Boolean(), nullable=False, server_default='false'))

def downgrade():
    op.drop_column('order', 'confirmed')