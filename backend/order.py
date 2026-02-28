from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from backend.models import db, Order, OrderItem, Cart, Product
from backend.email import send_order_confirmation
from datetime import datetime
import random
import string

bp = Blueprint('order', __name__)

def generate_order_number():
    prefix = 'ORD'
    timestamp = datetime.now().strftime('%Y%m%d')
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{timestamp}-{random_chars}"

@bp.route('/create', methods=['POST'])
def create_order():
    data = request.get_json()
    
    # Get cart items
    if current_user.is_authenticated:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create order
        order = Order(
            order_number=generate_order_number(),
            user_id=current_user.id,
            total_amount=total,
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            status='pending'
        )
        db.session.add(order)
        db.session.flush()
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Update stock
            product = cart_item.product
            product.stock -= cart_item.quantity
        
        # Clear cart
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
    else:
        # Guest user
        cart = session.get('cart', {})
        if not cart:
            return jsonify({'error': 'Cart is empty'}), 400
        
        total = 0
        order_items = []
        
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                total += product.price * quantity
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': product.price
                })
        
        # Create order for guest
        order = Order(
            order_number=generate_order_number(),
            total_amount=total,
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            status='pending'
        )
        db.session.add(order)
        db.session.flush()
        
        # Create order items
        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
            
            # Update stock
            item['product'].stock -= item['quantity']
        
        db.session.commit()
        session.pop('cart', None)
    
    # Send confirmation email
    if current_user.is_authenticated and current_user.email:
        try:
            send_order_confirmation(order)
        except:
            pass
    
    return jsonify({
        'message': 'Order created successfully',
        'order': order.to_dict()
    }), 201

@bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    if current_user.is_authenticated:
        order = Order.query.filter_by(
            id=order_id, 
            user_id=current_user.id
        ).first_or_404()
    else:
        # For guest, check session (simplified)
        order = Order.query.get_or_404(order_id)
    
    return jsonify(order.to_dict())

@bp.route('/history', methods=['GET'])
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id)\
        .order_by(Order.created_at.desc()).all()
    return jsonify([order.to_dict() for order in orders])

@bp.route('/update-status/<int:order_id>', methods=['PUT'])
@login_required
def update_status(order_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    order = Order.query.get_or_404(order_id)
    order.status = data.get('status', order.status)
    
    db.session.commit()
    return jsonify({'message': 'Order status updated'})

@bp.route('/track/<order_number>', methods=['GET'])
def track_order(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    return jsonify({
        'order_number': order.order_number,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'estimated_delivery': '3-5 business days'
    })
