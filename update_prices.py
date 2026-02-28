from backend import create_app, db
from backend.models import Product

app = create_app()

with app.app_context():
    # Update all products with reasonable prices (under 3500)
    products = Product.query.all()
    
    price_updates = {
        # Watches
        'Submariner Date': 2999,
        'Daytona Cosmograph': 3499,
        'Speedmaster Moonwatch': 2799,
        'Seamaster Aqua Terra': 2299,
        'Carrera Calibre 16': 1899,
        'Aquaracer': 1599,
        'Santos de Cartier': 3199,
        'Tank Française': 2499,
        
        # Gold Jewelry
        'Gold Chain Necklace': 899,
        'Gold Cuban Bracelet': 599,
        'Gold Hoop Earrings': 399,
        'Gold Signet Ring': 499,
        'Gold Pendant': 349,
        'Gold Bangle': 449,
        
        # Diamond Jewelry
        'Diamond Engagement Ring': 2499,
        'Diamond Stud Earrings': 1299,
        'Diamond Tennis Bracelet': 1999,
        'Diamond Pendant': 899,
        'Diamond Eternity Ring': 1699,
        'Diamond Cocktail Ring': 2199,
        
        # Other
        'Pearl Necklace': 399,
        'Sapphire Ring': 1499,
        'Emerald Earrings': 1799,
        'Ruby Pendant': 1599
    }
    
    updated_count = 0
    for product in products:
        if product.name in price_updates:
            old_price = product.price
            product.price = price_updates[product.name]
            print(f"✅ {product.name}: KES {old_price} → KES {product.price}")
            updated_count += 1
    
    db.session.commit()
    print(f"\n🎉 Updated {updated_count} products successfully!")
    
    # Show all products with new prices
    print("\n📊 Current Products:")
    print("-" * 60)
    for product in Product.query.order_by(Product.category, Product.price).all():
        print(f"{product.name:30} {product.category:10} KES {product.price}")
