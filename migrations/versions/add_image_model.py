"""Add image model and relationships

Revision ID: add_image_model
Revises: previous_revision
Create Date: 2025-10-12

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'add_image_model'
down_revision = None  # Change this to your last migration's revision ID
branch_labels = None
depends_on = None

def upgrade():
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
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['uploaded_by'], ['user.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index for faster lookups
    op.create_index('idx_image_product', 'image', ['product_id'])
    op.create_index('idx_image_shop', 'image', ['shop_id'])
    op.create_index('idx_image_uploaded_by', 'image', ['uploaded_by'])
    
    # Add uploads directory
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