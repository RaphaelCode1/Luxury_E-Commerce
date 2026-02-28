from backend import create_app, db
import sqlalchemy as sa
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    # Check if column exists
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('orders')]
    
    if 'checkout_request_id' not in columns:
        print("Adding checkout_request_id column to orders table...")
        
        # Add column using raw SQL
        with db.engine.connect() as conn:
            conn.execute(sa.text('ALTER TABLE orders ADD COLUMN checkout_request_id VARCHAR(100)'))
            conn.commit()
        print("✅ Added checkout_request_id column")
    else:
        print("✅ checkout_request_id column already exists")
    
    # Verify
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('orders')]
    print(f"\n📊 Orders table columns: {columns}")
