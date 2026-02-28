from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    CORS(app)
    
    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from backend.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from backend.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from backend.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from backend.order import bp as order_bp
    app.register_blueprint(order_bp, url_prefix='/orders')
    
    from backend.cart import bp as cart_bp
    app.register_blueprint(cart_bp, url_prefix='/cart')
    
    # Register M-Pesa payment blueprint
    try:
        from backend.api.mpesa_payment import bp as mpesa_payment_bp
        app.register_blueprint(mpesa_payment_bp)
        print("✅ M-Pesa payment blueprint registered")
    except ImportError as e:
        print(f"⚠️ M-Pesa payment blueprint not loaded: {e}")
    
    # Register direct routes
    from backend.routes import register_routes
    register_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        from backend.models import User
        admin = User.query.filter_by(email='admin@luxurytime.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@luxurytime.com',
                phone='254700000000',
                is_admin=True,
                email_verified=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created: admin@luxurytime.com / admin123")
    
    return app
