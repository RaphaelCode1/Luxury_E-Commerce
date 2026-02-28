from flask import jsonify, request
from backend.models import Product

def get_products():
    """Get all products with optional filtering"""
    category = request.args.get('category')
    brand = request.args.get('brand')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    if brand:
        query = query.filter_by(brand=brand)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    
    products = query.all()
    return jsonify([p.to_dict() for p in products])

def get_product(id):
    """Get single product by ID"""
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

def get_by_category(category):
    """Get products by category"""
    products = Product.query.filter_by(category=category).all()
    return jsonify([p.to_dict() for p in products])

def search_products():
    """Search products by name or brand"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    products = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) | 
        (Product.brand.ilike(f'%{query}%'))
    ).all()
    
    return jsonify([p.to_dict() for p in products])

def get_featured():
    """Get featured products"""
    products = Product.query.filter_by(featured=True).limit(6).all()
    return jsonify([p.to_dict() for p in products])
