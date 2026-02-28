import jwt
from flask import current_app
from time import time
from backend.models import User

def generate_token(user_id, expires_in=3600):
    return jwt.encode(
        {'user_id': user_id, 'exp': time() + expires_in},
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def verify_token(token):
    try:
        data = jwt.decode(
            token, 
            current_app.config['SECRET_KEY'], 
            algorithms=['HS256']
        )
        return User.query.get(data['user_id'])
    except:
        return None

def generate_email_verification_token(user_id):
    return jwt.encode(
        {'verify_email': user_id, 'exp': time() + 86400},  # 24 hours
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )
