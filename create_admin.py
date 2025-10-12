from ecommerce import create_app, db
from ecommerce.models.user import User

def create_admin_user(username='admin', email='admin@quickshop.com', password='admin123'):
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(role='admin').first()
        
        if admin:
            # Update existing admin password
            admin.set_password(password)
            print(f"\nUpdated existing admin account:")
            print(f"Username: {admin.username}")
            print(f"Email: {admin.email}")
            print(f"Password: {password}")
        else:
            # Create new admin user
            admin = User(username=username, email=email, role='admin')
            admin.set_password(password)
            admin.is_active = True
            db.session.add(admin)
            print(f"\nCreated new admin account:")
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Password: {password}")
        
        try:
            db.session.commit()
            print("Admin account saved successfully!")
            print("\nYou can now log in to the admin dashboard with these credentials.")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating/updating admin account: {str(e)}")

if __name__ == '__main__':
    print("Creating/Updating Admin Account...")
    create_admin_user()