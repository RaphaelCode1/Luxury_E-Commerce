// Checkout functionality

// Validate checkout form
function validateCheckoutForm() {
    const form = document.getElementById('checkout-form');
    if (!form) return true;
    
    const required = ['fullname', 'email', 'phone', 'address', 'city'];
    let isValid = true;
    
    required.forEach(field => {
        const input = form.querySelector(`[name="${field}"]`);
        if (!input.value.trim()) {
            input.classList.add('error');
            isValid = false;
        } else {
            input.classList.remove('error');
        }
    });
    
    // Validate email
    const email = form.querySelector('[name="email"]');
    if (email && email.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value)) {
            email.classList.add('error');
            isValid = false;
        }
    }
    
    // Validate phone (Kenyan format)
    const phone = form.querySelector('[name="phone"]');
    if (phone && phone.value) {
        const phoneRegex = /^(0|254|2540)?[7][0-9]{8}$/;
        if (!phoneRegex.test(phone.value.replace(/\s/g, ''))) {
            phone.classList.add('error');
            isValid = false;
        }
    }
    
    if (!isValid) {
        showNotification('Please fill all fields correctly', 'error');
    }
    
    return isValid;
}

// Format phone for M-Pesa
function formatPhoneForMpesa(phone) {
    // Remove all non-digits
    phone = phone.replace(/\D/g, '');
    
    // Convert to 254 format
    if (phone.startsWith('0')) {
        phone = '254' + phone.substring(1);
    } else if (phone.startsWith('7')) {
        phone = '254' + phone;
    }
    
    return phone;
}

// Place order
function placeOrder(event) {
    event.preventDefault();
    
    if (!validateCheckoutForm()) {
        return;
    }
    
    const formData = new FormData(document.getElementById('checkout-form'));
    const orderData = {
        fullname: formData.get('fullname'),
        email: formData.get('email'),
        phone: formatPhoneForMpesa(formData.get('phone')),
        address: formData.get('address'),
        city: formData.get('city'),
        cart: getCart(),
        total: calculateTotal()
    };
    
    // Store order data for payment page
    localStorage.setItem('currentOrder', JSON.stringify(orderData));
    
    // Redirect to payment
    window.location.href = '/payment/mpesa';
}

// Load order summary on payment page
function loadOrderSummary() {
    const orderData = JSON.parse(localStorage.getItem('currentOrder'));
    const summaryElement = document.getElementById('order-summary');
    
    if (!orderData || !summaryElement) return;
    
    summaryElement.innerHTML = `
        <h3>Order Summary</h3>
        <p><strong>Name:</strong> ${orderData.fullname}</p>
        <p><strong>Phone:</strong> ${orderData.phone}</p>
        <p><strong>Total:</strong> ${formatPrice(orderData.total)}</p>
    `;
}

// Initialize payment
function initPayment() {
    const orderData = JSON.parse(localStorage.getItem('currentOrder'));
    if (!orderData) {
        window.location.href = '/cart/view';
        return;
    }
    
    document.getElementById('payment-amount').textContent = formatPrice(orderData.total);
    document.getElementById('payment-phone').textContent = orderData.phone;
}

// Process M-Pesa payment
function processMpesaPayment() {
    const orderData = JSON.parse(localStorage.getItem('currentOrder'));
    
    showLoading('#payment-button');
    
    // Simulate API call
    setTimeout(() => {
        hideLoading('#payment-button', 'Processing...');
        
        // Simulate STK Push
        showNotification('STK Push sent to your phone. Please enter PIN.', 'info');
        
        // Simulate callback after 5 seconds
        setTimeout(() => {
            // Generate random receipt number
            const receipt = 'MP' + Math.random().toString(36).substring(2, 10).toUpperCase();
            
            // Store receipt
            localStorage.setItem('mpesaReceipt', receipt);
            localStorage.setItem('paymentStatus', 'success');
            
            // Clear cart
            localStorage.removeItem('cart');
            
            // Redirect to success
            window.location.href = '/payment/success?receipt=' + receipt;
        }, 5000);
    }, 2000);
}
