from flask_mail import Message
from backend import mail
from flask import current_app, render_template
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Email error: {e}")

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_welcome_email(user):
    send_email(
        'Welcome to LUXURYTIME!',
        [user.email],
        f'Welcome {user.username}! Thank you for registering.',
        render_template('email/welcome_email.html', user=user)
    )

def send_password_reset_email(user, token):
    send_email(
        'Password Reset Request',
        [user.email],
        f'Click the link to reset your password: {current_app.config["BASE_URL"]}/auth/reset-password/{token}',
        render_template('email/password_reset.html', user=user, token=token)
    )

def send_order_confirmation(order):
    send_email(
        f'Order Confirmation #{order.order_number}',
        [order.customer.email],
        f'Thank you for your order! Total: KES {order.total_amount:,.0f}',
        render_template('email/order_confirmation.html', order=order)
    )
