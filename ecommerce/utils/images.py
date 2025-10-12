import os
import uuid
from PIL import Image as PILImage
from werkzeug.utils import secure_filename
from flask import current_app
from ..models.image import Image
from .. import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def generate_unique_filename(original_filename):
    """Generate a unique filename while preserving the original extension"""
    ext = get_file_extension(original_filename)
    return f"{uuid.uuid4().hex}.{ext}"

def save_image(file, uploaded_by, product_id=None, shop_id=None):
    """
    Save an uploaded image file and create database record
    
    Args:
        file: FileStorage object from request.files
        uploaded_by: User ID who uploaded the file
        product_id: Optional ID of associated product
        shop_id: Optional ID of associated shop
    
    Returns:
        Image model instance if successful, None if failed
    """
    if not file or not allowed_file(file.filename):
        return None
        
    try:
        # Generate secure filename
        original_filename = secure_filename(file.filename)
        filename = generate_unique_filename(original_filename)
        
        # Create upload directory if it doesn't exist
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        
        # Full path for the file
        file_path = os.path.join(upload_path, filename)
        
        # Open and validate image
        img = PILImage.open(file)
        width, height = img.size
        
        # Save the image
        img.save(file_path, optimize=True, quality=85)
        
        # Get file size
        size = os.path.getsize(file_path)
        
        if size > MAX_IMAGE_SIZE:
            os.remove(file_path)
            return None
            
        # Create database record
        image = Image(
            filename=filename,
            original_filename=original_filename,
            mime_type=file.content_type,
            size=size,
            width=width,
            height=height,
            uploaded_by=uploaded_by,
            product_id=product_id,
            shop_id=shop_id
        )
        
        db.session.add(image)
        db.session.commit()
        
        return image
        
    except Exception as e:
        current_app.logger.error(f"Error saving image: {str(e)}")
        # Clean up file if it was created
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return None

def delete_image(image_id):
    """
    Delete an image and its file
    
    Args:
        image_id: ID of the image to delete
    
    Returns:
        Boolean indicating success
    """
    try:
        image = Image.query.get(image_id)
        if not image:
            return False
            
        # Delete file
        file_path = os.path.join(current_app.root_path, 'static', 'uploads', image.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # Delete database record
        db.session.delete(image)
        db.session.commit()
        
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error deleting image: {str(e)}")
        return False

def get_image_url(image):
    """Get the URL for an image"""
    if not image:
        return None
    return f"/static/uploads/{image.filename}"