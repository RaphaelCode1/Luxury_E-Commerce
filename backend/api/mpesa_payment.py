from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from backend.models import db, Order
import json
import os

bp = Blueprint('mpesa_payment', __name__, url_prefix='/api/mpesa')

@bp.route('/stkpush', methods=['POST'])
@login_required
def stk_push():
    """Initiate STK Push payment"""
    try:
        data = request.get_json()
        
        phone = data.get('phone')
        amount = data.get('amount')
        order_id = data.get('order_id')
        
        if not phone or not amount or not order_id:
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # For now, return simulated success
        checkout_id = f"ws_CO_{order_id}_{hash(phone) % 10000}"
        
        # Try to update order if it exists
        try:
            order = Order.query.get(int(order_id))
            if order:
                order.checkout_request_id = checkout_id
                db.session.commit()
                print(f"✅ Updated order {order_id} with checkout ID: {checkout_id}")
        except Exception as e:
            print(f"⚠️ Could not update order: {e}")
        
        return jsonify({
            'success': True,
            'message': 'STK Push sent. Please check your phone.',
            'checkout_request_id': checkout_id,
            'merchant_request_id': f"MR_{order_id}"
        })
            
    except Exception as e:
        print(f"STK Push error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/status/<checkout_id>', methods=['GET'])
def payment_status(checkout_id):
    """Check payment status"""
    try:
        # Simulate status response
        return jsonify({
            'success': True,
            'status': 'completed',
            'result_code': '0',
            'result_desc': 'The service was accepted successfully',
            'checkout_id': checkout_id
        })
    except Exception as e:
        print(f"Status error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@bp.route('/callback', methods=['POST'])
def callback():
    """Handle M-Pesa callback"""
    try:
        callback_data = request.get_json()
        print("📞 M-Pesa Callback received:", json.dumps(callback_data, indent=2))
        
        # Extract callback info if present
        if callback_data and 'Body' in callback_data:
            stk_callback = callback_data['Body'].get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')
            checkout_id = stk_callback.get('CheckoutRequestID')
            
            print(f"   Result Code: {result_code}")
            print(f"   Checkout ID: {checkout_id}")
            
            # Try to update order
            if checkout_id:
                try:
                    order = Order.query.filter_by(checkout_request_id=checkout_id).first()
                    if order:
                        if result_code == 0:
                            order.status = 'paid'
                            print(f"✅ Payment successful for order {order.id}")
                        else:
                            order.status = 'failed'
                            print(f"❌ Payment failed for order {order.id}")
                        db.session.commit()
                except Exception as e:
                    print(f"⚠️ Could not update order: {e}")
        
        # Always return success to M-Pesa
        return jsonify({
            'ResultCode': 0,
            'ResultDesc': 'Success'
        })
        
    except Exception as e:
        print(f"Callback error: {e}")
        return jsonify({
            'ResultCode': 1,
            'ResultDesc': str(e)
        }), 500
