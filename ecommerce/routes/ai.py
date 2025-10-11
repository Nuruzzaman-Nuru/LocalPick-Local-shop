from flask import Blueprint, render_template, request, jsonify
from ..models.shop import Product
from .. import db
from ..utils.ai.negotiation_bot import create_negotiation_session

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


@ai_bp.route('/')
def assistant():
    """Render a minimal AI assistant page for negotiating on a product."""
    return render_template('ai/assistant.html')


@ai_bp.route('/negotiate', methods=['POST'])
def negotiate():
    """API endpoint to run the local negotiation bot for a product.

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
