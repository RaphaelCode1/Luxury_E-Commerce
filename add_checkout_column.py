from backend import create_app, db
import sqlite3
import os

app = create_app()

with app.app_context():
    # Check if we're using SQLite
    db_path = 'ecommerce.db'
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get column info for orders table
        cursor.execute("PRAGMA table_info(orders)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print("Current columns in orders table:", column_names)
        
        if 'checkout_request_id' not in column_names:
            cursor.execute("ALTER TABLE orders ADD COLUMN checkout_request_id VARCHAR(100)")
            print("✅ Added checkout_request_id column to orders table")
        else:
            print("ℹ️ checkout_request_id column already exists")
        
        conn.commit()
        conn.close()
    else:
        print("📝 Database doesn't exist yet - will be created on first run")
        
    # Also update the Order model in code
    from backend.models import Order
    if not hasattr(Order, 'checkout_request_id'):
        print("⚠️ Order model needs to be updated - restart after this script")
