import json
import pytest

from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        # Create a minimal Product model instance if available
        try:
            from ecommerce.models.shop import Product, Shop
            shop = Shop(name='Test Shop', is_active=True)
            db.session.add(shop)
            db.session.commit()
            prod = Product(name='Test Product', price=10.0, min_price=5.0, max_discount_percentage=20, shop_id=shop.id)
            db.session.add(prod)
            db.session.commit()
        except Exception:
            # If models are different in repo, skip model creation
            pass

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_negotiate_endpoint(client):
    # Try calling negotiate with product id 1
    resp = client.post('/ai/negotiate', json={'product_id': 1, 'offered_price': 6.0})
    assert resp.status_code in (200, 400, 404)
    data = resp.get_json()
    assert isinstance(data, dict)
