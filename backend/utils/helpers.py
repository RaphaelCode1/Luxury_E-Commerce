import re
from datetime import datetime
import random
import string

def format_price(amount):
    """Format price to KES with commas"""
    return f"KES {amount:,.0f}"

def validate_phone(phone):
    """Validate and format Kenyan phone number"""
    # Remove all non-digits
    phone = re.sub(r'\D', '', phone)
    
    # Convert to 254 format
    if phone.startswith('0'):
        phone = '254' + phone[1:]
    elif phone.startswith('7'):
        phone = '254' + phone
    
    # Validate length
    if len(phone) != 12 or not phone.startswith('2547'):
        return None
    
    return phone

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_order_number():
    """Generate unique order number"""
    prefix = 'ORD'
    timestamp = datetime.now().strftime('%Y%m%d')
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{timestamp}-{random_chars}"

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def get_cart_count(user, session):
    """Get cart count for current user"""
    from backend.models import Cart
    
    if user.is_authenticated:
        return Cart.query.filter_by(user_id=user.id).count()
    else:
        return sum(session.get('cart', {}).values())

def calculate_cart_total(cart_items):
    """Calculate total from cart items"""
    total = 0
    for item in cart_items:
        if hasattr(item, 'product'):
            total += item.product.price * item.quantity
        else:
            total += item['price'] * item['quantity']
    return total
