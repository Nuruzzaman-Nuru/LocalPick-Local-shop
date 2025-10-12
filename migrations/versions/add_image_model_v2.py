"""Add image model and relationships

Revision ID: add_image_model_v2
Revises: add_image_model
Create Date: 2025-10-13

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'add_image_model_v2'
down_revision = 'add_image_model'  # Use your last migration's revision ID
branch_labels = None
depends_on = None

def upgrade():
    # Drop old images table if it exists
    try:
        op.drop_table('image')
    except:
        pass
    
    # Create images table
    op.create_table(
        'image',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('original_filename', sa.String(255), nullable=False),
        sa.Column('mime_type', sa.String(100), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('uploaded_by', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('shop_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['uploaded_by'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('idx_image_product', 'image', ['product_id'])
    op.create_index('idx_image_shop', 'image', ['shop_id'])
    op.create_index('idx_image_uploaded_by', 'image', ['uploaded_by'])
    
    # Create uploads directory if it doesn't exist
    import os
    from flask import current_app
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

def downgrade():
    # Remove indices
    op.drop_index('idx_image_product')
    op.drop_index('idx_image_shop')
    op.drop_index('idx_image_uploaded_by')
    
    # Remove table
    op.drop_table('image')