from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from ..models.shop import Product
from .. import db
try:
    from ..utils.ai.negotiation_bot import create_negotiation_session
except Exception:
    def create_negotiation_session(*args, **kwargs):
        class DummyBot:
            def evaluate_offer(self, amount):
                return ('reject', None, 'AI unavailable')
        return DummyBot()

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({
                'status': 'error',
                'message': 'Access denied. Admin privileges required.'
            }), 403
        return f(*args, **kwargs)
    return decorated_function

@ai_bp.route('/')
@login_required
@admin_required
def assistant():
    """Render a minimal AI assistant page for negotiating on a product."""
    return render_template('ai/assistant.html')


@ai_bp.route('/negotiate', methods=['POST'])
@login_required
@admin_required
def negotiate():
    """API endpoint to run the local negotiation bot for a product.
    Admin only endpoint.

    Expects JSON: { product_id: int, offered_price: float }
    Returns JSON with decision/counter/message.
    """
    data = request.get_json() or {}
    product_id = data.get('product_id')
    offered_price = data.get('offered_price')

    if product_id is None or offered_price is None:
        return jsonify({'status': 'error', 'message': 'product_id and offered_price are required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'status': 'error', 'message': 'Product not found'}), 404

    # Make sure the product is negotiable at model level if available
    try:
        bot = create_negotiation_session(product)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

    decision, counter, message = bot.evaluate_offer(float(offered_price))

    return jsonify({
        'status': 'success',
        'decision': decision,
        'counter_price': counter,
        'message': message
    })
