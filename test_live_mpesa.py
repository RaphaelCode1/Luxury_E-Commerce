from backend import create_app
from mpesa.mpesa_config import MpesaConfig
import os

# Create Flask app
app = create_app()

with app.app_context():
    print("=" * 60)
    print("TESTING M-PESA WITH LIVE CREDENTIALS")
    print("=" * 60)
    
    # Test 1: Check if credentials are loaded
    consumer_key = app.config.get('MPESA_CONSUMER_KEY')
    consumer_secret = app.config.get('MPESA_CONSUMER_SECRET')
    
    print(f"\n📋 Configuration Check:")
    print(f"   Consumer Key: {consumer_key[:10]}... (loaded)")
    print(f"   Consumer Secret: {consumer_secret[:10]}... (loaded)")
    print(f"   Passkey: {app.config.get('MPESA_PASSKEY')[:10]}... (loaded)")
    print(f"   Shortcode: {app.config.get('MPESA_SHORTCODE')}")
    
    # Test 2: Generate password
    print(f"\n🔐 Testing Password Generation:")
    password, timestamp = MpesaConfig.generate_password()
    print(f"   Timestamp: {timestamp}")
    print(f"   Password: {password[:30]}...")
    
    # Test 3: Try to get access token
    print(f"\n🔄 Attempting to get Access Token...")
    token = MpesaConfig.get_access_token()
    
    if token:
        print(f"   ✅ SUCCESS! Access Token obtained:")
        print(f"   Token: {token[:30]}...")
    else:
        print(f"   ❌ Failed to get access token")
        print(f"   Please check your credentials and internet connection")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
