<<<<<<< HEAD
import os
from ecommerce import create_app

app = create_app(os.getenv('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
=======
import os
from ecommerce import create_app

app = create_app(os.getenv('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
>>>>>>> 1829c7bf62e855be81dcdd6bc733a8863b82f360
    app.run(host='0.0.0.0', port=4000)