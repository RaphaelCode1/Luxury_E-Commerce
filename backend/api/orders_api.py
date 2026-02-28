from flask import jsonify, request, session
from flask_login import login_required, current_user
from backend.models import db, Order, OrderItem, Cart, Product
from backend.utils.helpers import generate_order_number, calculate_cart_total
from backend.email import send_order_confirmation

def create_order():
    """Create a new order from cart"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
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
        except Exception as e:
            print(f"Email error: {e}")
    
    return jsonify({
        'message': 'Order created successfully',
        'order': {
            'order_number': order.order_number,
            'total': order.total_amount,
            'status': order.status
        }
    }), 201

def get_order(order_id):
    """Get order by ID"""
    if current_user.is_authenticated:
        order = Order.query.filter_by(
            id=order_id, 
            user_id=current_user.id
        ).first_or_404()
    else:
        order = Order.query.get_or_404(order_id)
    
    return jsonify(order.to_dict())

def get_order_history():
    """Get user's order history"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please login to view orders'}), 401
    
    orders = Order.query.filter_by(user_id=current_user.id)\
        .order_by(Order.created_at.desc()).all()
    
    return jsonify([order.to_dict() for order in orders])

def update_order_status(order_id):
    """Update order status (admin only)"""
    if not current_user.is_authenticated or not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    order = Order.query.get_or_404(order_id)
    order.status = data.get('status', order.status)
    
    db.session.commit()
    return jsonify({'message': 'Order status updated'})
