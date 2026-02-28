#!/usr/bin/env python3
print("Checking installation...\n")

# Check imports
try:
    from flask import Flask
    print("✅ Flask installed")
except ImportError as e:
    print(f"❌ Flask: {e}")

try:
    from backend.models import db
    print("✅ Models import")
except ImportError as e:
    print(f"❌ Models: {e}")

try:
    from backend.utils.helpers import generate_order_number
    test_num = generate_order_number()
    print(f"✅ helpers.generate_order_number: {test_num}")
except ImportError as e:
    print(f"❌ helpers: {e}")

try:
    from backend.api.orders_api import create_order
    print("✅ orders_api import")
except ImportError as e:
    print(f"❌ orders_api: {e}")

print("\nAll checks complete!")
