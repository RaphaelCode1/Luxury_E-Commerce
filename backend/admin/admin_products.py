from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from backend.admin import bp
from backend.models import db, Product
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Configure upload folder
UPLOAD_FOLDER = 'frontend/static/images/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/products')
@login_required
def list_products():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    query = Product.query
    
    if category != 'all':
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    products = query.order_by(Product.created_at.desc()).all()
    
    return render_template('admin/products_list.html', products=products)

@bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        return render_template('admin/product_form.html')
    
    # Handle POST request
    data = request.form
    
    # Handle image upload
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid duplicates
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Ensure directory exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Save file
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = f'/static/images/products/{filename}'
    
    # Create product
    product = Product(
        name=data.get('name'),
        brand=data.get('brand'),
        category=data.get('category'),
        description=data.get('description'),
        price=float(data.get('price', 0)),
        discount=float(data.get('discount', 0)),
        image_url=image_url,
        stock=int(data.get('stock', 0)),
        featured=bool(data.get('featured', False))
    )
    
    db.session.add(product)
    db.session.commit()
    
    return redirect(url_for('admin.list_products'))

@bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    product = Product.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/product_form.html', product=product)
    
    # Handle POST request
    data = request.form
    
    product.name = data.get('name', product.name)
    product.brand = data.get('brand', product.brand)
    product.category = data.get('category', product.category)
    product.description = data.get('description', product.description)
    product.price = float(data.get('price', product.price))
    product.discount = float(data.get('discount', product.discount))
    product.stock = int(data.get('stock', product.stock))
    product.featured = bool(data.get('featured', product.featured))
    
    # Handle image upload
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            product.image_url = f'/static/images/products/{filename}'
    
    db.session.commit()
    
    return redirect(url_for('admin.list_products'))

@bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    product = Product.query.get_or_404(id)
    
    # Delete image file if exists
    if product.image_url:
        filename = product.image_url.split('/')[-1]
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted successfully'})

@bp.route('/products/bulk-discount', methods=['POST'])
@login_required
def bulk_discount():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    category = data.get('category', 'all')
    discount = float(data.get('discount', 0))
    
    query = Product.query
    if category != 'all':
        query = query.filter_by(category=category)
    
    products = query.all()
    for product in products:
        product.discount = discount
    
    db.session.commit()
    
    return jsonify({
        'message': f'✅ Applied {discount}% discount to {len(products)} products in {category} category'
    })
