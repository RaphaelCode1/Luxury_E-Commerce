from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from backend.models import db, Cart, Product

bp = Blueprint('cart', __name__)

@bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    product = Product.query.get_or_404(product_id)
    
    if product.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    if current_user.is_authenticated:
        # User is logged in - save to database
        cart_item = Cart.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        return jsonify({'message': 'Added to cart', 'cart_count': get_cart_count()}), 200
    else:
        # Guest user - use session
        cart = session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        session['cart'] = cart
        return jsonify({'message': 'Added to cart', 'cart_count': sum(cart.values())}), 200

@bp.route('/', methods=['GET'])
def get_cart():
    items = []
    total = 0
    
    if current_user.is_authenticated:
        # Get from database
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        for item in cart_items:
            product = item.product
            items.append({
                'id': item.id,
                'product_id': product.id,
                'name': product.name,
                'brand': product.brand,
                'price': product.price,
                'image': product.image_url,
                'quantity': item.quantity,
                'total': product.price * item.quantity
            })
            total += product.price * item.quantity
    else:
        # Get from session
        cart = session.get('cart', {})
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                items.append({
                    'product_id': product.id,
                    'name': product.name,
                    'brand': product.brand,
                    'price': product.price,
                    'image': product.image_url,
                    'quantity': quantity,
                    'total': product.price * quantity
                })
                total += product.price * quantity
    
    return jsonify({
        'items': items,
        'total': total,
        'count': len(items)
    })

@bp.route('/update/<int:item_id>', methods=['PUT'])
def update_cart(item_id):
    data = request.get_json()
    quantity = data.get('quantity')
    
    if current_user.is_authenticated:
        cart_item = Cart.query.get_or_404(item_id)
        if quantity <= 0:
            db.session.delete(cart_item)
        else:
            cart_item.quantity = quantity
        db.session.commit()
    else:
        cart = session.get('cart', {})
        if quantity <= 0:
            cart.pop(str(item_id), None)
        else:
            cart[str(item_id)] = quantity
        session['cart'] = cart
    
    return jsonify({'message': 'Cart updated', 'cart_count': get_cart_count()}), 200

@bp.route('/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    if current_user.is_authenticated:
        cart_item = Cart.query.get_or_404(item_id)
        db.session.delete(cart_item)
        db.session.commit()
    else:
        cart = session.get('cart', {})
        cart.pop(str(item_id), None)
        session['cart'] = cart
    
    return jsonify({'message': 'Item removed', 'cart_count': get_cart_count()}), 200

@bp.route('/clear', methods=['POST'])
def clear_cart():
    if current_user.is_authenticated:
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
    else:
        session.pop('cart', None)
    
    return jsonify({'message': 'Cart cleared'}), 200

def get_cart_count():
    if current_user.is_authenticated:
        return Cart.query.filter_by(user_id=current_user.id).count()
    else:
        return sum(session.get('cart', {}).values())
