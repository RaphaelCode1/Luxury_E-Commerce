from flask import jsonify
from backend.models import Order

def track_order(order_number):
    """Track order by order number"""
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    
    return jsonify({
        'order_number': order.order_number,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'estimated_delivery': '3-5 business days',
        'items': [{
            'product': item.product.name,
            'quantity': item.quantity,
            'price': item.price
        } for item in order.items]
    })
