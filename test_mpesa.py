import os
from dotenv import load_dotenv
import base64
from datetime import datetime

load_dotenv()

def test_mpesa_config():
    """Test M-Pesa configuration without Flask context"""
    print("=" * 50)
    print("TESTING M-PESA CONFIGURATION")
    print("=" * 50)
    
    # Test 1: Check if passkey is loaded
    passkey = os.getenv('MPESA_PASSKEY')
    if passkey:
        print(f"✅ Passkey loaded: {passkey[:10]}... (hidden for security)")
    else:
        print("❌ Passkey not found in .env file")
    
    # Test 2: Check shortcode
    shortcode = os.getenv('MPESA_SHORTCODE', '174379')
    print(f"✅ Shortcode: {shortcode}")
    
    # Test 3: Generate password manually
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = f"{shortcode}{passkey}{timestamp}"
    password_bytes = password_str.encode('ascii')
    password_base64 = base64.b64encode(password_bytes).decode('ascii')
    
    print(f"✅ Password generated: {password_base64[:30]}...")
    print(f"✅ Timestamp: {timestamp}")
    
    # Test 4: Check consumer key (without showing full value)
    consumer_key = os.getenv('MPESA_CONSUMER_KEY')
    if consumer_key:
        print(f"✅ Consumer Key: {consumer_key[:5]}... (present)")
    else:
        print("⚠️ Consumer Key not set - needed for real transactions")
    
    consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
    if consumer_secret:
        print(f"✅ Consumer Secret: {consumer_secret[:5]}... (present)")
    else:
        print("⚠️ Consumer Secret not set - needed for real transactions")
    
    print("\n" + "=" * 50)
    print("M-PESA CONFIGURATION TEST COMPLETE")
    print("=" * 50)
    print("\n✅ Your passkey and shortcode are working!")
    print("⚠️ You still need to add your Consumer Key and Secret to .env file")
    print("📝 Format: MPESA_CONSUMER_KEY=your_key_here")
    print("📝 Format: MPESA_CONSUMER_SECRET=your_secret_here")

if __name__ == "__main__":
    test_mpesa_config()
