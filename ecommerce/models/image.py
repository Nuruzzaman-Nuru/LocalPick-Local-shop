from datetime import datetime
from .. import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)  # File size in bytes
    width = db.Column(db.Integer)  # Image width in pixels
    height = db.Column(db.Integer)  # Image height in pixels
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=True)
    
    def __init__(self, filename, original_filename, mime_type, size, uploaded_by, width=None, height=None, product_id=None, shop_id=None):
        self.filename = filename
        self.original_filename = original_filename
        self.mime_type = mime_type
        self.size = size
        self.width = width
        self.height = height
        self.uploaded_by = uploaded_by
        self.product_id = product_id
        self.shop_id = shop_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'mime_type': self.mime_type,
            'size': self.size,
            'width': self.width,
            'height': self.height,
            'uploaded_by': self.uploaded_by,
            'product_id': self.product_id,
            'shop_id': self.shop_id,
            'created_at': self.created_at.isoformat()
        }