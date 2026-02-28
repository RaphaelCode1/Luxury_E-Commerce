from backend import create_app, db
import sqlalchemy as sa
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    # Check if discount column exists in products table
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('products')]
    
    if 'discount' not in columns:
        print("Adding discount column to products table...")
        
        # Add column using raw SQL
        with db.engine.connect() as conn:
            conn.execute(sa.text('ALTER TABLE products ADD COLUMN discount FLOAT DEFAULT 0'))
            conn.commit()
        print("✅ Added discount column")
    else:
        print("✅ discount column already exists")
    
    # Verify
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('products')]
    print(f"\n📊 Products table columns: {columns}")
