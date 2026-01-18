<<<<<<< HEAD
from ecommerce import create_app, db

app = create_app()

with app.app_context():

    with db.engine.connect() as conn:
        conn.execute('ALTER TABLE user ADD COLUMN email_notifications BOOLEAN DEFAULT TRUE')
        conn.commit()

print("Database updated successfully!")
=======
from ecommerce import create_app, db

app = create_app()

with app.app_context():

    with db.engine.connect() as conn:
        conn.execute('ALTER TABLE user ADD COLUMN email_notifications BOOLEAN DEFAULT TRUE')
        conn.commit()

print("Database updated successfully!")
>>>>>>> 1829c7bf62e855be81dcdd6bc733a8863b82f360
