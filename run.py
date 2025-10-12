import os
from ecommerce import create_app

# Flask app তৈরি
app = create_app(os.getenv('FLASK_CONFIG', 'development'))

# Entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
