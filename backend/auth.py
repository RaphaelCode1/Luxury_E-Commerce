from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from backend.models import User, db
from backend.email import send_welcome_email, send_password_reset_email
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    
    data = request.get_json() if request.is_json else request.form
    
    email = data.get('email')
    password = data.get('password')
    remember = data.get('remember', False)
    
    if not email or not password:
        if request.is_json:
            return jsonify({'error': 'Email and password required'}), 400
        flash('Email and password required', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        login_user(user, remember=remember)
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin
        
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        
        if request.is_json:
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_admin': user.is_admin
                }
            }), 200
        else:
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
    
    if request.is_json:
        return jsonify({'error': 'Invalid email or password'}), 401
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    
    data = request.get_json() if request.is_json else request.form
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    
    if not username or not email or not password:
        if request.is_json:
            return jsonify({'error': 'Missing required fields'}), 400
        flash('All fields are required', 'error')
        return redirect(url_for('auth.register'))
    
    if User.query.filter_by(email=email).first():
        if request.is_json:
            return jsonify({'error': 'Email already registered'}), 400
        flash('Email already registered', 'error')
        return redirect(url_for('auth.register'))
    
    user = User(
        username=username,
        email=email,
        phone=phone
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    if request.is_json:
        return jsonify({'message': 'Registration successful'}), 201
    else:
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html', user=current_user)
