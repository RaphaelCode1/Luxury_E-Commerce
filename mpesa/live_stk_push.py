import requests
import json
from flask import current_app
from mpesa.mpesa_config import MpesaConfig

def send_stk_push(phone_number, amount, order_id, account_reference="LuxuryTime"):
    """
    Send STK Push to customer's phone using live credentials
    """
    try:
        # Get access token
        access_token = MpesaConfig.get_access_token()
        if not access_token:
            return {
                'success': False,
                'error': 'Failed to get access token',
                'message': 'Authentication failed'
            }
        
        # Generate password and timestamp
        password, timestamp = MpesaConfig.generate_password()
        
        # Format phone number (ensure it's in 254 format)
        original_phone = phone_number
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number.startswith('7'):
            phone_number = '254' + phone_number
        
        # Prepare STK push payload
        payload = {
            'BusinessShortCode': current_app.config['MPESA_SHORTCODE'],
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(amount),
            'PartyA': phone_number,
            'PartyB': current_app.config['MPESA_SHORTCODE'],
            'PhoneNumber': phone_number,
            'CallBackURL': f"{current_app.config['BASE_URL']}/api/mpesa/callback",
            'AccountReference': account_reference[:12],
            'TransactionDesc': f'Payment for Order {order_id}'
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Make the request
        response = requests.post(
            current_app.config['MPESA_STK_PUSH_URL'],
            json=payload,
            headers=headers,
            timeout=30
        )
        
        result = response.json()
        
        if response.status_code == 200:
            return {
                'success': True,
                'message': 'STK Push sent successfully',
                'checkout_request_id': result.get('CheckoutRequestID'),
                'merchant_request_id': result.get('MerchantRequestID'),
                'response_code': result.get('ResponseCode'),
                'response_description': result.get('ResponseDescription'),
                'raw_response': result
            }
        else:
            return {
                'success': False,
                'error': result.get('errorMessage', 'STK Push failed'),
                'response_code': response.status_code,
                'raw_response': result
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': 'Network error',
            'message': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': 'Unexpected error',
            'message': str(e)
        }

def query_status(checkout_request_id):
    """
    Query the status of a payment
    """
    try:
        access_token = MpesaConfig.get_access_token()
        if not access_token:
            return {'success': False, 'error': 'Failed to get access token'}
        
        password, timestamp = MpesaConfig.generate_password()
        
        payload = {
            'BusinessShortCode': current_app.config['MPESA_SHORTCODE'],
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            current_app.config['MPESA_QUERY_URL'],
            json=payload,
            headers=headers,
            timeout=30
        )
        
        result = response.json()
        
        if response.status_code == 200:
            return {
                'success': True,
                'data': result
            }
        else:
            return {
                'success': False,
                'error': result.get('errorMessage', 'Query failed'),
                'raw_response': result
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
