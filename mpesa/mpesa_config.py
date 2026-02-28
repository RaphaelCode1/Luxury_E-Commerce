import base64
import requests
from datetime import datetime
from flask import current_app
import os

class MpesaConfig:
    @staticmethod
    def get_access_token():
        """Get OAuth access token from Safaricom"""
        consumer_key = current_app.config.get('MPESA_CONSUMER_KEY') or os.getenv('MPESA_CONSUMER_KEY')
        consumer_secret = current_app.config.get('MPESA_CONSUMER_SECRET') or os.getenv('MPESA_CONSUMER_SECRET')
        
        if not consumer_key or not consumer_secret:
            print("Error: M-Pesa consumer key or secret not set")
            return None
            
        auth_string = f"{consumer_key}:{consumer_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_base64}'
        }
        
        try:
            auth_url = current_app.config.get('MPESA_AUTH_URL', 
                'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials')
            response = requests.get(auth_url, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result.get('access_token')
        except requests.exceptions.RequestException as e:
            print(f"Request error getting access token: {e}")
            return None
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    @staticmethod
    def generate_password():
        """Generate password for STK push"""
        shortcode = current_app.config.get('MPESA_SHORTCODE', '174379')
        passkey = current_app.config.get('MPESA_PASSKEY') or os.getenv('MPESA_PASSKEY')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        password_str = f"{shortcode}{passkey}{timestamp}"
        password_bytes = password_str.encode('ascii')
        password_base64 = base64.b64encode(password_bytes).decode('ascii')
        
        return password_base64, timestamp
