from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from backend.admin import bp
from backend.models import User, Product, Order, db
from datetime import datetime, timedelta

@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get statistics
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    
    # Recent orders (last 10)
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Revenue this month
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    monthly_revenue = db.session.query(db.func.sum(Order.total_amount))\
        .filter(Order.created_at >= month_start)\
        .filter(Order.status == 'paid')\
        .scalar() or 0
    
    # Low stock products (stock < 5)
    low_stock_products = Product.query.filter(Product.stock < 5).count()
    
    # Pending orders
    pending_orders = Order.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         recent_orders=recent_orders,
                         monthly_revenue=int(monthly_revenue),
                         low_stock_products=low_stock_products,
                         pending_orders=pending_orders)

@bp.route('/api/stats')
@login_required
def get_stats():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Orders by status
    orders_by_status = db.session.query(
        Order.status, db.func.count(Order.id)
    ).group_by(Order.status).all()
    
    # Revenue by day (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    daily_revenue = db.session.query(
        db.func.date(Order.created_at),
        db.func.sum(Order.total_amount)
    ).filter(Order.created_at >= seven_days_ago)\
     .filter(Order.status == 'paid')\
     .group_by(db.func.date(Order.created_at)).all()
    
    return jsonify({
        'orders_by_status': dict(orders_by_status),
        'daily_revenue': [{'date': str(d), 'revenue': float(r) if r else 0} for d, r in daily_revenue]
    })

@bp.route('/quick-stats')
@login_required
def quick_stats():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get quick stats for dashboard widgets
    today = datetime.now().date()
    today_orders = Order.query.filter(
        db.func.date(Order.created_at) == today
    ).count()
    
    today_revenue = db.session.query(db.func.sum(Order.total_amount))\
        .filter(db.func.date(Order.created_at) == today)\
        .filter(Order.status == 'paid')\
        .scalar() or 0
    
    return jsonify({
        'today_orders': today_orders,
        'today_revenue': int(today_revenue),
        'low_stock': Product.query.filter(Product.stock < 5).count(),
        'pending_orders': Order.query.filter_by(status='pending').count()
    })
