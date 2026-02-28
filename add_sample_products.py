from backend import create_app, db
from backend.models import Product

app = create_app()

with app.app_context():
    # Clear existing products
    Product.query.delete()
    
    # Add sample products
    products = [
        Product(
            name='Submariner Date',
            brand='Rolex',
            category='watches',
            description='The iconic Rolex Submariner Date with black ceramic bezel. Features automatic movement, 300m water resistance, and Oystersteel construction.',
            price=1450000,
            image_url='/static/images/products/watches/rolex-submariner.jpg',
            stock=5,
            featured=True
        ),
        Product(
            name='Daytona Cosmograph',
            brand='Rolex',
            category='watches',
            description='The legendary Rolex Daytona Cosmograph chronograph. Features tachymeter bezel and Oystersteel construction.',
            price=2200000,
            image_url='/static/images/products/watches/rolex-daytona.jpg',
            stock=3,
            featured=True
        ),
        Product(
            name='Speedmaster Moonwatch',
            brand='Omega',
            category='watches',
            description='The legendary Omega Speedmaster Moonwatch, the first watch worn on the moon. Features manual-winding chronograph movement.',
            price=1100000,
            image_url='/static/images/products/watches/omega-speedmaster.jpg',
            stock=4,
            featured=True
        ),
        Product(
            name='Seamaster Aqua Terra',
            brand='Omega',
            category='watches',
            description='Omega Seamaster Aqua Terra with blue dial and Co-Axial movement. Water resistant to 150m.',
            price=850000,
            image_url='/static/images/products/watches/omega-seamaster.jpg',
            stock=6,
            featured=False
        ),
        Product(
            name='Carrera Calibre 16',
            brand='Tag Heuer',
            category='watches',
            description='Tag Heuer Carrera Calibre 16 chronograph with black dial and leather strap.',
            price=520000,
            image_url='/static/images/products/watches/tag-carrera.jpg',
            stock=8,
            featured=True
        ),
        Product(
            name='Santos de Cartier',
            brand='Cartier',
            category='watches',
            description='Cartier Santos de Cartier with steel and gold construction. Iconic square case design.',
            price=1650000,
            image_url='/static/images/products/watches/cartier-santos.jpg',
            stock=2,
            featured=True
        ),
        Product(
            name='Gold Chain Necklace',
            brand='Luxury Gold',
            category='gold',
            description='18K Gold chain necklace, Figaro link, 20 inches. Perfect for everyday wear.',
            price=185000,
            image_url='/static/images/products/gold/gold-necklace.jpg',
            stock=10,
            featured=True
        ),
        Product(
            name='Gold Cuban Bracelet',
            brand='Luxury Gold',
            category='gold',
            description='18K Gold Cuban link bracelet, 8 inches. Heavy weight, solid construction.',
            price=120000,
            image_url='/static/images/products/gold/gold-bracelet.jpg',
            stock=7,
            featured=False
        ),
        Product(
            name='Diamond Engagement Ring',
            brand='Luxury Diamonds',
            category='diamond',
            description='1 carat solitaire diamond engagement ring in platinum. GIA certified.',
            price=650000,
            image_url='/static/images/products/diamond/engagement-ring.jpg',
            stock=3,
            featured=True
        ),
        Product(
            name='Diamond Stud Earrings',
            brand='Luxury Diamonds',
            category='diamond',
            description='0.5 carat each diamond stud earrings in 18K white gold. Brilliant cut.',
            price=320000,
            image_url='/static/images/products/diamond/diamond-earrings.jpg',
            stock=5,
            featured=False
        )
    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    print(f"✅ Added {len(products)} sample products to database")
    
    # Verify products were added
    count = Product.query.count()
    print(f"✅ Total products in database: {count}")
