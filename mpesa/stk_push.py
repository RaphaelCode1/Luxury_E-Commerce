import requests
from flask import current_app
from mpesa.mpesa_config import MpesaConfig

def initiate_stk_push(phone_number, amount, order_id, account_reference="LuxuryTime"):
    """
    Initiate STK Push to customer's phone
    """
    try:
        # Get access token
        access_token = MpesaConfig.get_access_token()
        if not access_token:
            return {
                'success': False,
                'message': 'Failed to get access token'
            }
        
        # Generate password and timestamp
        password, timestamp = MpesaConfig.generate_password()
        
        # Format phone number (ensure it's in 254 format)
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number.startswith('7'):
            phone_number = '254' + phone_number
        
        # Prepare STK push payload
        payload = {
            'BusinessShortCode': current_app.config.get('MPESA_SHORTCODE', '174379'),
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(amount),
            'PartyA': phone_number,
            'PartyB': current_app.config.get('MPESA_SHORTCODE', '174379'),
            'PhoneNumber': phone_number,
            'CallBackURL': f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/mpesa/callback",
            'AccountReference': account_reference[:12],
            'TransactionDesc': f'Payment for order {order_id}'
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Make the request
        response = requests.post(
            current_app.config.get('MPESA_STK_PUSH_URL', 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'),
            json=payload,
            headers=headers,
            timeout=30
        )
        
        result = response.json()
        
        if response.status_code == 200:
            return {
                'success': True,
                'message': 'STK Push sent successfully',
                'data': result
            }
        else:
            return {
                'success': False,
                'message': result.get('errorMessage', 'STK Push failed'),
                'data': result
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }

def query_payment_status(checkout_request_id):
    """
    Query the status of a payment
    """
    try:
        access_token = MpesaConfig.get_access_token()
        if not access_token:
            return {'success': False, 'message': 'Failed to get access token'}
        
        password, timestamp = MpesaConfig.generate_password()
        
        payload = {
            'BusinessShortCode': current_app.config.get('MPESA_SHORTCODE', '174379'),
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            current_app.config.get('MPESA_QUERY_URL', 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'),
            json=payload,
            headers=headers,
            timeout=30
        )
        
        return {
            'success': True,
            'data': response.json()
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }
