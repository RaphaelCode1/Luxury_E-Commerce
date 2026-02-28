from flask import jsonify, request, session
from flask_login import current_user
from backend.models import db, Cart, Product

def get_cart():
    """Get current user's cart"""
    if current_user.is_authenticated:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        items = []
        total = 0
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
        return jsonify({'items': items, 'total': total, 'count': len(items)})
    else:
        cart = session.get('cart', {})
        items = []
        total = 0
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
        return jsonify({'items': items, 'total': total, 'count': len(items)})

def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    product = Product.query.get_or_404(product_id)
    
    if product.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    if current_user.is_authenticated:
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
    else:
        cart = session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        session['cart'] = cart
    
    return jsonify({'message': 'Added to cart', 'cart_count': get_cart_count()})

def update_cart_item(item_id):
    """Update cart item quantity"""
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
    
    return jsonify({'message': 'Cart updated'})

def remove_from_cart(item_id):
    """Remove item from cart"""
    if current_user.is_authenticated:
        cart_item = Cart.query.get_or_404(item_id)
        db.session.delete(cart_item)
        db.session.commit()
    else:
        cart = session.get('cart', {})
        cart.pop(str(item_id), None)
        session['cart'] = cart
    
    return jsonify({'message': 'Item removed'})

def get_cart_count():
    """Get total items in cart"""
    if current_user.is_authenticated:
        return Cart.query.filter_by(user_id=current_user.id).count()
    else:
        return sum(session.get('cart', {}).values())
