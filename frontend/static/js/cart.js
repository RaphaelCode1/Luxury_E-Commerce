// Cart functionality

// Get cart from localStorage
function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

// Save cart to localStorage
function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    updateCartDisplay();
}

// Add item to cart
function addToCart(productId) {
    const cart = getCart();
    const existingItem = cart.find(item => item.id === productId);
    
    // Find product details (you'd normally get this from API)
    const product = findProductById(productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: product.name,
            brand: product.brand,
            price: product.price,
            image: product.image,
            quantity: 1
        });
    }
    
    saveCart(cart);
    showNotification('Product added to cart!', 'success');
}

// Remove item from cart
function removeFromCart(productId) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== productId);
    saveCart(cart);
    showNotification('Item removed from cart', 'info');
}

// Update item quantity
function updateQuantity(productId, newQuantity) {
    const cart = getCart();
    const item = cart.find(item => item.id === productId);
    
    if (item) {
        if (newQuantity <= 0) {
            removeFromCart(productId);
            return;
        }
        item.quantity = newQuantity;
        saveCart(cart);
    }
}

// Calculate cart total
function calculateTotal() {
    const cart = getCart();
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
}

// Update cart display
function updateCartDisplay() {
    const cartContainer = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    
    if (!cartContainer) return;
    
    const cart = getCart();
    
    if (cart.length === 0) {
        cartContainer.innerHTML = '<tr><td colspan="5" class="empty-cart">Your cart is empty</td></tr>';
        if (cartTotal) cartTotal.textContent = formatPrice(0);
        return;
    }
    
    let html = '';
    cart.forEach(item => {
        html += `
            <tr>
                <td><img src="${item.image}" alt="${item.name}" width="50" height="50"></td>
                <td>${item.brand} ${item.name}</td>
                <td>${formatPrice(item.price)}</td>
                <td>
                    <input type="number" value="${item.quantity}" min="1" 
                           onchange="updateQuantity(${item.id}, parseInt(this.value))">
                </td>
                <td>${formatPrice(item.price * item.quantity)}</td>
                <td><button onclick="removeFromCart(${item.id})" class="btn-remove">Remove</button></td>
            </tr>
        `;
    });
    
    cartContainer.innerHTML = html;
    if (cartTotal) cartTotal.textContent = formatPrice(calculateTotal());
}

// Clear cart
function clearCart() {
    if (confirm('Are you sure you want to clear your cart?')) {
        localStorage.removeItem('cart');
        saveCart([]);
        showNotification('Cart cleared', 'info');
    }
}

// Helper function to find product by ID
function findProductById(id) {
    const allProducts = [
        { id: 1, name: 'Submariner Date', brand: 'Rolex', price: 1450000, image: '/static/images/products/watches/rolex-submariner.jpg' },
        { id: 2, name: 'Daytona Cosmograph', brand: 'Rolex', price: 2200000, image: '/static/images/products/watches/rolex-daytona.jpg' },
        { id: 3, name: 'Speedmaster Moonwatch', brand: 'Omega', price: 1100000, image: '/static/images/products/watches/omega-speedmaster.jpg' },
        { id: 7, name: 'Gold Chain Necklace', brand: 'Luxury Gold', price: 185000, image: '/static/images/products/gold/gold-necklace.jpg' },
        { id: 10, name: 'Diamond Engagement Ring', brand: 'Luxury Diamonds', price: 650000, image: '/static/images/products/diamond/engagement-ring.jpg' }
    ];
    return allProducts.find(p => p.id === id) || { name: 'Product', brand: 'Luxury', price: 0, image: '' };
}
