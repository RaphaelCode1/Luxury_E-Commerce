from backend import create_app, db
import sqlite3

app = create_app()

with app.app_context():
    # Add discount column to Product table if it doesn't exist
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('ALTER TABLE products ADD COLUMN discount FLOAT DEFAULT 0')
        print("✅ Added discount column to products table")
    except sqlite3.OperationalError:
        print("ℹ️ Discount column already exists")
    
    conn.commit()
    conn.close()
    
    print("✅ Database updated successfully")
