from backend import create_app, db
from backend.models import Product
import sqlite3
import os

app = create_app()

with app.app_context():
    # Check if discount column exists
    db_path = 'ecommerce.db'
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get column info
        cursor.execute("PRAGMA table_info(products)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'discount' not in column_names:
            cursor.execute("ALTER TABLE products ADD COLUMN discount FLOAT DEFAULT 0")
            print("✅ Added discount column to products table")
        else:
            print("ℹ️ Discount column already exists")
        
        conn.commit()
        conn.close()
    else:
        print("📝 Database will be created on first run")
