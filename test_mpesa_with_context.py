from backend import create_app
from mpesa.mpesa_config import MpesaConfig
import os

# Create Flask app
app = create_app()

with app.app_context():
    print("=" * 50)
    print("TESTING M-PESA WITH FLASK CONTEXT")
    print("=" * 50)
    
    # Test 1: Generate password
    password, timestamp = MpesaConfig.generate_password()
    print(f"✅ Password generated: {password[:30]}...")
    print(f"✅ Timestamp: {timestamp}")
    
    # Test 2: Try to get access token (will fail without keys)
    print("\n" + "-" * 30)
    print("Attempting to get access token...")
    token = MpesaConfig.get_access_token()
    if token:
        print(f"✅ Access token: {token[:20]}...")
    else:
        print("⚠️ Could not get access token - missing Consumer Key/Secret")
        print("   This is expected until you add your credentials")
    
    print("\n" + "=" * 50)
    print("TEST COMPLETE")
    print("=" * 50)
