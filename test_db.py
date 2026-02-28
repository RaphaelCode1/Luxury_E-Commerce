from backend import create_app, db
from backend.models import User
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Test connection - use text() for raw SQL
        result = db.session.execute(text('SELECT 1')).scalar()
        print(f"✅ MySQL connection successful! Test query result: {result}")
        
        # Check tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Existing tables: {tables}")
        
        # Create tables if needed
        db.create_all()
        print("✅ Tables created/verified")
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@luxurytime.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@luxurytime.com',
                phone='254700000000',
                is_admin=True,
                email_verified=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created")
        else:
            print("✅ Admin user already exists")
        
        # Count users
        user_count = User.query.count()
        print(f"👥 Total users: {user_count}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
