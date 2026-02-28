from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from backend.admin import bp
from backend.models import db, Order

@bp.route('/orders')
@login_required
def list_orders():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    status = request.args.get('status')
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    # For API response
    if request.headers.get('Accept') == 'application/json':
        return jsonify([order.to_dict() for order in orders])
    
    # For HTML template
    return render_template('admin/orders_list.html', orders=orders)

@bp.route('/orders/<int:id>')
@login_required
def view_order(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    order = Order.query.get_or_404(id)
    
    if request.headers.get('Accept') == 'application/json':
        return jsonify(order.to_dict())
    
    return render_template('admin/order_detail.html', order=order)

@bp.route('/orders/update-status/<int:id>', methods=['POST', 'PUT'])
@login_required
def update_order_status(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json() if request.is_json else request.form
    order = Order.query.get_or_404(id)
    order.status = data.get('status', order.status)
    
    db.session.commit()
    
    return jsonify({'message': 'Order status updated', 'status': order.status})
