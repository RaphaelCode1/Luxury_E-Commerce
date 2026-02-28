from flask import jsonify, request
from flask_login import login_required, current_user
from backend.models import db

def get_profile():
    """Get current user profile"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'phone': current_user.phone,
        'address': current_user.address,
        'city': current_user.city,
        'is_admin': current_user.is_admin
    })

def update_profile():
    """Update current user profile"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    
    if 'phone' in data:
        current_user.phone = data['phone']
    if 'address' in data:
        current_user.address = data['address']
    if 'city' in data:
        current_user.city = data['city']
    
    db.session.commit()
    
    return jsonify({'message': 'Profile updated successfully'})
