from flask import render_template, send_from_directory, redirect, url_for
from backend.models import Product
import os

def register_routes(app):
    @app.route('/')
    def index():
        """Homepage"""
        try:
            featured_products = Product.query.filter_by(featured=True).limit(6).all()
            return render_template('index.html', featured_products=featured_products)
        except Exception as e:
            print(f"Error in index: {e}")
            return render_template('index.html', featured_products=[])
    
    @app.route('/products/watches')
    def watches():
        return render_template('products/list.html', category='watches')
    
    @app.route('/products/gold')
    def gold():
        return render_template('products/list.html', category='gold')
    
    @app.route('/products/diamond')
    def diamond():
        return render_template('products/list.html', category='diamond')
    
    @app.route('/product/<int:id>')
    def product_detail(id):
        """Product detail page"""
        product = Product.query.get_or_404(id)
        return render_template('products/detail.html', product=product)
    
    @app.route('/about')
    def about():
        return render_template('content/about.html')
    
    @app.route('/contact')
    def contact():
        return render_template('content/contact.html')
    
    # Cart routes
    @app.route('/cart')
    def cart_redirect():
        """Redirect /cart to /cart/view"""
        return redirect(url_for('cart_view'))
    
    @app.route('/cart/view')
    def cart_view():
        """View shopping cart"""
        return render_template('cart/view.html')
    
    @app.route('/cart/checkout')
    def cart_checkout():
        """Checkout page"""
        return render_template('cart/checkout.html')
    
    # Payment routes
    @app.route('/payment/mpesa')
    def mpesa_payment():
        """M-Pesa payment page"""
        return render_template('payment/mpesa.html')
    
    @app.route('/payment/success')
    def payment_success():
        """Payment success page"""
        return render_template('payment/success.html')
    
    @app.route('/payment/failed')
    def payment_failed():
        """Payment failed page"""
        return render_template('payment/failed.html')
    
    # User routes
    @app.route('/user/login')
    def user_login():
        """User login page"""
        return render_template('user/login.html')
    
    @app.route('/user/register')
    def user_register():
        """User registration page"""
        return render_template('user/register.html')
    
    @app.route('/user/profile')
    def user_profile():
        """User profile page"""
        return render_template('user/profile.html')
    
    @app.route('/user/orders')
    def user_orders():
        """User orders page"""
        return render_template('user/orders.html')
    
    # Static file serving
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        static_dir = os.path.join(root_dir, 'frontend', 'static')
        return send_from_directory(static_dir, filename)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from backend import db
        db.session.rollback()
        return render_template('500.html'), 500

    @app.route("/payment/mpesa-test")
    def mpesa_test():
        """M-Pesa test page"""
        return render_template("payment/mpesa_test.html")

    @app.route("/payment/mpesa-simple")
    def mpesa_simple():
        """M-Pesa simple test page"""
        return render_template("payment/mpesa_simple.html")
