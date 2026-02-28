from flask import Blueprint
from backend.api import products, users, cart_api, orders_api, password_reset, tracking

bp = Blueprint('api', __name__)

# Product routes
bp.add_url_rule('/products', view_func=products.get_products, methods=['GET'])
bp.add_url_rule('/products/<int:id>', view_func=products.get_product, methods=['GET'])
bp.add_url_rule('/products/category/<category>', view_func=products.get_by_category, methods=['GET'])
bp.add_url_rule('/products/search', view_func=products.search_products, methods=['GET'])
bp.add_url_rule('/products/featured', view_func=products.get_featured, methods=['GET'])

# User routes
bp.add_url_rule('/users/profile', view_func=users.get_profile, methods=['GET'])
bp.add_url_rule('/users/profile', view_func=users.update_profile, methods=['PUT'])

# Cart routes
bp.add_url_rule('/cart', view_func=cart_api.get_cart, methods=['GET'])
bp.add_url_rule('/cart/add', view_func=cart_api.add_to_cart, methods=['POST'])
bp.add_url_rule('/cart/update/<int:item_id>', view_func=cart_api.update_cart_item, methods=['PUT'])
bp.add_url_rule('/cart/remove/<int:item_id>', view_func=cart_api.remove_from_cart, methods=['DELETE'])

# Order routes
bp.add_url_rule('/orders', view_func=orders_api.create_order, methods=['POST'])
bp.add_url_rule('/orders/history', view_func=orders_api.get_order_history, methods=['GET'])
bp.add_url_rule('/orders/<int:order_id>', view_func=orders_api.get_order, methods=['GET'])
bp.add_url_rule('/orders/<int:order_id>/status', view_func=orders_api.update_order_status, methods=['PUT'])

# Tracking routes
bp.add_url_rule('/tracking/<order_number>', view_func=tracking.track_order, methods=['GET'])

# Password reset routes
bp.add_url_rule('/password-reset/request', view_func=password_reset.request_reset, methods=['POST'])
bp.add_url_rule('/password-reset/<token>', view_func=password_reset.reset_password, methods=['POST'])
