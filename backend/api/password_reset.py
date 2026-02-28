from flask import jsonify, request
from backend.models import User
from backend.email import send_password_reset_email

def request_reset():
    """Request password reset email"""
    data = request.get_json()
    email = data.get('email')
    
    user = User.query.filter_by(email=email).first()
    if user:
        token = user.get_reset_token()
        send_password_reset_email(user, token)
    
    # Always return success to prevent email enumeration
    return jsonify({'message': 'If email exists, reset link has been sent'}), 200

def reset_password(token):
    """Reset password with token"""
    data = request.get_json()
    password = data.get('password')
    
    user = User.verify_reset_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 400
    
    user.set_password(password)
    user.email_verified = True
    db.session.commit()
    
    return jsonify({'message': 'Password reset successful'}), 200
