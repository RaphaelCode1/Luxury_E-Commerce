import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///ecommerce.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # M-Pesa Config
    MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY', 'test')
    MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET', 'test')
    MPESA_PASSKEY = os.getenv('MPESA_PASSKEY', 'test')
    MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE', '174379')
    MPESA_ENVIRONMENT = 'sandbox'
    
    # Email Config
    MAIL_SERVER = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER', '')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    
    # Base URL
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

    # M-Pesa URLs (Sandbox)
    MPESA_AUTH_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    MPESA_STK_PUSH_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    MPESA_QUERY_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
