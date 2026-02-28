from backend import create_app, db
from backend.models import Product

app = create_app()

with app.app_context():
    # Clear existing products
    Product.query.delete()
    
    # Add sample products (without discount field)
    products = [
        # Watches
        Product(
            name='Submariner Date',
            brand='Rolex',
            category='watches',
            description='The iconic Rolex Submariner Date with black ceramic bezel. Features automatic movement, 300m water resistance, and Oystersteel construction.',
            price=2999,
            image_url='/static/images/products/watches/rolex-submariner.jpg',
            stock=10,
            featured=True
        ),
        Product(
            name='Daytona Cosmograph',
            brand='Rolex',
            category='watches',
            description='The legendary Rolex Daytona Cosmograph chronograph. Features tachymeter bezel and Oystersteel construction.',
            price=3499,
            image_url='/static/images/products/watches/rolex-daytona.jpg',
            stock=5,
            featured=True
        ),
        Product(
            name='Speedmaster Moonwatch',
            brand='Omega',
            category='watches',
            description='The legendary Omega Speedmaster Moonwatch, the first watch worn on the moon. Features manual-winding chronograph movement.',
            price=2799,
            image_url='/static/images/products/watches/omega-speedmaster.jpg',
            stock=8,
            featured=True
        ),
        Product(
            name='Seamaster Aqua Terra',
            brand='Omega',
            category='watches',
            description='Omega Seamaster Aqua Terra with blue dial and Co-Axial movement. Water resistant to 150m.',
            price=2299,
            image_url='/static/images/products/watches/omega-seamaster.jpg',
            stock=12,
            featured=False
        ),
        Product(
            name='Carrera Calibre 16',
            brand='Tag Heuer',
            category='watches',
            description='Tag Heuer Carrera Calibre 16 chronograph with black dial and leather strap.',
            price=1899,
            image_url='/static/images/products/watches/tag-carrera.jpg',
            stock=15,
            featured=True
        ),
        Product(
            name='Santos de Cartier',
            brand='Cartier',
            category='watches',
            description='Cartier Santos de Cartier with steel and gold construction. Iconic square case design.',
            price=3199,
            image_url='/static/images/products/watches/cartier-santos.jpg',
            stock=4,
            featured=True
        ),
        
        # Gold Jewelry
        Product(
            name='Gold Chain Necklace',
            brand='Luxury Gold',
            category='gold',
            description='18K Gold chain necklace, Figaro link, 20 inches. Perfect for everyday wear.',
            price=899,
            image_url='/static/images/products/gold/gold-necklace.jpg',
            stock=20,
            featured=True
        ),
        Product(
            name='Gold Cuban Bracelet',
            brand='Luxury Gold',
            category='gold',
            description='18K Gold Cuban link bracelet, 8 inches. Heavy weight, solid construction.',
            price=599,
            image_url='/static/images/products/gold/gold-bracelet.jpg',
            stock=15,
            featured=True
        ),
        Product(
            name='Gold Hoop Earrings',
            brand='Luxury Gold',
            category='gold',
            description='18K Gold hoop earrings, medium size. Screw-back closure.',
            price=399,
            image_url='/static/images/products/gold/gold-earrings.jpg',
            stock=25,
            featured=False
        ),
        
        # Diamond Jewelry
        Product(
            name='Diamond Engagement Ring',
            brand='Luxury Diamonds',
            category='diamond',
            description='1 carat solitaire diamond engagement ring in platinum. GIA certified, brilliant cut.',
            price=2499,
            image_url='/static/images/products/diamond/engagement-ring.jpg',
            stock=5,
            featured=True
        ),
        Product(
            name='Diamond Stud Earrings',
            brand='Luxury Diamonds',
            category='diamond',
            description='0.5 carat each diamond studs in 18K white gold. Screw-back setting.',
            price=1299,
            image_url='/static/images/products/diamond/diamond-earrings.jpg',
            stock=8,
            featured=True
        ),
        Product(
            name='Diamond Tennis Bracelet',
            brand='Luxury Diamonds',
            category='diamond',
            description='3 carat total diamond tennis bracelet. 18K white gold, secure clasp.',
            price=1999,
            image_url='/static/images/products/diamond/tennis-bracelet.jpg',
            stock=6,
            featured=False
        ),
    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    print(f"✅ Added {len(products)} sample products to database")
    
    # Show products by category
    print("\n📋 Products by Category:")
    print("-" * 50)
    categories = {}
    for p in Product.query.all():
        if p.category not in categories:
            categories[p.category] = []
        categories[p.category].append(p)
    
    for category, items in categories.items():
        print(f"\n{category.upper()}:")
        for item in items:
            print(f"  • {item.name}: KES {item.price}")
    
    # API test
    print(f"\n🌐 API Endpoint: http://localhost:5001/api/products")
    print(f"   Run: curl http://localhost:5001/api/products | python -m json.tool")
