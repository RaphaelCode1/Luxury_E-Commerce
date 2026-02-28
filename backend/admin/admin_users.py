from flask import render_template, jsonify
from flask_login import login_required, current_user
from backend.admin import bp
from backend.models import User, db

@bp.route('/users')
@login_required
def list_users():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users_list.html', users=users)

@bp.route('/users/<int:id>')
@login_required
def view_user(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'address': user.address,
        'city': user.city,
        'is_admin': user.is_admin,
        'email_verified': user.email_verified,
        'created_at': user.created_at.isoformat(),
        'orders': [{
            'order_number': o.order_number,
            'total': o.total_amount,
            'status': o.status,
            'date': o.created_at.isoformat()
        } for o in user.orders]
    })

@bp.route('/users/toggle-admin/<int:id>', methods=['POST'])
@login_required
def toggle_admin(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    return jsonify({'message': 'User admin status updated', 'is_admin': user.is_admin})
