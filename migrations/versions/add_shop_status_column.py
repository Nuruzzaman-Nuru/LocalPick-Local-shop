"""add_shop_status_column

Revision ID: add_shop_status_column
Revises: add_location_updated_at
Create Date: 2024-01-05 14:05:22.123456

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_shop_status_column'
down_revision = 'add_location_updated_at'
branch_labels = None
depends_on = None

def upgrade():
    # Add approval_status column with default value 'pending'
    op.add_column('shop', sa.Column('approval_status', sa.String(20), server_default='pending'))

def downgrade():
    op.drop_column('shop', 'approval_status')