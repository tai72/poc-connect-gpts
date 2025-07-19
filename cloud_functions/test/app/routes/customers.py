from flask import Blueprint, request, jsonify, current_app

customers_bp = Blueprint('customers', __name__)


@customers_bp.route('/', methods=['GET'])
def get_customers():
    auth_header = request.headers.get('Authorization', '')
    expected_token = f"Bearer {current_app.config['API_KEY']}"

    if auth_header != expected_token:
        return jsonify({"error": "Forbidden"}), 403

    customers = ["Alice", "Bob", "Charlie"]
    return jsonify({"customers": customers})
