// Products JavaScript

// Sample product data (replace with API calls later)
const sampleProducts = {
    watches: [
        { id: 1, name: 'Submariner Date', brand: 'Rolex', price: 1450000, image: '/static/images/products/watches/rolex-submariner.jpg', category: 'watches' },
        { id: 2, name: 'Daytona Cosmograph', brand: 'Rolex', price: 2200000, image: '/static/images/products/watches/rolex-daytona.jpg', category: 'watches' },
        { id: 3, name: 'Speedmaster Moonwatch', brand: 'Omega', price: 1100000, image: '/static/images/products/watches/omega-speedmaster.jpg', category: 'watches' },
        { id: 4, name: 'Seamaster Aqua Terra', brand: 'Omega', price: 850000, image: '/static/images/products/watches/omega-seamaster.jpg', category: 'watches' },
        { id: 5, name: 'Carrera Calibre 16', brand: 'Tag Heuer', price: 520000, image: '/static/images/products/watches/tag-carrera.jpg', category: 'watches' },
        { id: 6, name: 'Santos de Cartier', brand: 'Cartier', price: 1650000, image: '/static/images/products/watches/cartier-santos.jpg', category: 'watches' }
    ],
    gold: [
        { id: 7, name: 'Gold Chain Necklace', brand: 'Luxury Gold', price: 185000, image: '/static/images/products/gold/gold-necklace.jpg', category: 'gold' },
        { id: 8, name: 'Gold Cuban Bracelet', brand: 'Luxury Gold', price: 120000, image: '/static/images/products/gold/gold-bracelet.jpg', category: 'gold' },
        { id: 9, name: 'Gold Hoop Earrings', brand: 'Luxury Gold', price: 95000, image: '/static/images/products/gold/gold-earrings.jpg', category: 'gold' }
    ],
    diamond: [
        { id: 10, name: 'Diamond Engagement Ring', brand: 'Luxury Diamonds', price: 650000, image: '/static/images/products/diamond/engagement-ring.jpg', category: 'diamond' },
        { id: 11, name: 'Diamond Stud Earrings', brand: 'Luxury Diamonds', price: 320000, image: '/static/images/products/diamond/diamond-earrings.jpg', category: 'diamond' },
        { id: 12, name: 'Diamond Tennis Bracelet', brand: 'Luxury Diamonds', price: 480000, image: '/static/images/products/diamond/tennis-bracelet.jpg', category: 'diamond' }
    ]
};

// Load products on page
function loadProducts(category = 'all') {
    const productGrid = document.getElementById('product-grid');
    if (!productGrid) return;
    
    let products = [];
    
    if (category === 'all') {
        products = [...sampleProducts.watches, ...sampleProducts.gold, ...sampleProducts.diamond];
    } else {
        products = sampleProducts[category] || [];
    }
    
    displayProducts(products);
}

// Display products in grid
function displayProducts(products) {
    const productGrid = document.getElementById('product-grid');
    if (!productGrid) return;
    
    productGrid.innerHTML = products.map(product => `
        <div class="product-card" data-id="${product.id}">
            <span class="product-badge">New</span>
            <img src="${product.image}" alt="${product.name}" class="product-image" onerror="this.src='/static/images/placeholder.jpg'">
            <div class="product-info">
                <div class="product-brand">${product.brand}</div>
                <h3 class="product-name">${product.name}</h3>
                <div class="product-price">${formatPrice(product.price)}</div>
                <button onclick="addToCart(${product.id})" class="btn btn-primary">Add to Cart</button>
                <a href="/product/${product.id}" class="btn btn-secondary">View Details</a>
            </div>
        </div>
    `).join('');
}

// Filter by category
function filterProducts(category) {
    // Update active tab
    document.querySelectorAll('.category-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Load products
    loadProducts(category);
}

// Search products
function searchProducts(query) {
    const allProducts = [...sampleProducts.watches, ...sampleProducts.gold, ...sampleProducts.diamond];
    const filtered = allProducts.filter(product => 
        product.name.toLowerCase().includes(query.toLowerCase()) ||
        product.brand.toLowerCase().includes(query.toLowerCase())
    );
    
    displayProducts(filtered);
}

// Sort products
function sortProducts(sortBy) {
    const productGrid = document.getElementById('product-grid');
    if (!productGrid) return;
    
    const products = Array.from(document.querySelectorAll('.product-card'));
    
    products.sort((a, b) => {
        const priceA = parseInt(a.querySelector('.product-price').textContent.replace(/[^0-9]/g, ''));
        const priceB = parseInt(b.querySelector('.product-price').textContent.replace(/[^0-9]/g, ''));
        
        if (sortBy === 'price-low') {
            return priceA - priceB;
        } else if (sortBy === 'price-high') {
            return priceB - priceA;
        }
    });
    
    productGrid.innerHTML = '';
    products.forEach(product => productGrid.appendChild(product));
}
