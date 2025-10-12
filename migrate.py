from ecommerce import db, create_app
from ecommerce.models.shop import Product, Shop
from sqlalchemy import text

def migrate():
    with db.engine.connect() as conn:
        # Add email_notifications column to user table with default value
        try:
            conn.execute(text('''
                ALTER TABLE user 
                ADD COLUMN email_notifications BOOLEAN NOT NULL DEFAULT 1
            '''))
            print("Added email_notifications column to user table")
        except Exception as e:
            print(f"Error adding email_notifications column (it might already exist): {e}")

        # Add category column to product table
        try:
            conn.execute(text('ALTER TABLE product ADD COLUMN category VARCHAR(50)'))
            print("Added category column to product table")
        except Exception as e:
            print(f"Error adding column (it might already exist): {e}")
            
        # Add about column to shop table
        try:
            conn.execute(text('ALTER TABLE shop ADD COLUMN about TEXT'))
            print("Added about column to shop table")
        except Exception as e:
            print(f"Error adding column (it might already exist): {e}")
        
        # Add contact fields to shop table
        try:
            conn.execute(text('ALTER TABLE shop ADD COLUMN phone VARCHAR(20)'))
            conn.execute(text('ALTER TABLE shop ADD COLUMN email VARCHAR(120)'))
            conn.execute(text('ALTER TABLE shop ADD COLUMN website VARCHAR(200)'))
            conn.execute(text('ALTER TABLE shop ADD COLUMN business_hours TEXT'))
            print("Added contact columns to shop table")
        except Exception as e:
            print(f"Error adding columns (they might already exist): {e}")
        
        # Add confirmed column to order table
        try:
            conn.execute(text('ALTER TABLE `order` ADD COLUMN confirmed BOOLEAN NOT NULL DEFAULT 0'))
            print("Added confirmed column to order table")
        except Exception as e:
            print(f"Error adding confirmed column (it might already exist): {e}")
            
        # Add approval_status column to shop table
        try:
            conn.execute(text('ALTER TABLE shop ADD COLUMN approval_status VARCHAR(20) NOT NULL DEFAULT \'pending\''))
            print("Added approval_status column to shop table")
        except Exception as e:
            print(f"Error adding approval_status column (it might already exist): {e}")
        
        # Add confirmed column to cart_item table
        try:
            conn.execute(text('ALTER TABLE cart_item ADD COLUMN confirmed BOOLEAN NOT NULL DEFAULT 0'))
            print("Added confirmed column to cart_item table")
        except Exception as e:
            print(f"Error adding confirmed column to cart_item table (it might already exist): {e}")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        migrate()