from flask import Blueprint

# Create blueprint
bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import routes after blueprint creation to avoid circular imports
from backend.admin import admin_dashboard, admin_products, admin_orders, admin_users
