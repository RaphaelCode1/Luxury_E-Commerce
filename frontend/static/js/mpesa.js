// M-Pesa frontend functionality

// Initialize M-Pesa payment
function initMpesaPayment(phone, amount, orderId) {
    const payload = {
        phone: phone,
        amount: amount,
        order_id: orderId
    };
    
    fetch('/api/mpesa/stkpush', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('STK Push sent. Check your phone.', 'success');
            checkPaymentStatus(data.checkoutRequestID);
        } else {
            showNotification('Payment failed: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Payment error', 'error');
    });
}

// Check payment status
function checkPaymentStatus(checkoutRequestID) {
    const checkInterval = setInterval(() => {
        fetch(`/api/mpesa/status/${checkoutRequestID}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'completed') {
                    clearInterval(checkInterval);
                    window.location.href = '/payment/success?receipt=' + data.receipt;
                } else if (data.status === 'failed') {
                    clearInterval(checkInterval);
                    window.location.href = '/payment/failed';
                }
            });
    }, 3000); // Check every 3 seconds
}

// Handle payment callback
function handlePaymentCallback(data) {
    if (data.ResultCode === 0) {
        // Payment successful
        const receipt = data.Result.Reference;
        localStorage.setItem('mpesaReceipt', receipt);
        
        // Update order status
        fetch(`/api/orders/update/${data.OrderID}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: 'paid',
                receipt: receipt
            })
        });
        
        // Clear cart
        localStorage.removeItem('cart');
        localStorage.removeItem('currentOrder');
        
        window.location.href = '/payment/success?receipt=' + receipt;
    } else {
        // Payment failed
        window.location.href = '/payment/failed?code=' + data.ResultCode;
    }
}

// Display payment status
function displayPaymentStatus() {
    const urlParams = new URLSearchParams(window.location.search);
    const receipt = urlParams.get('receipt');
    const code = urlParams.get('code');
    
    if (receipt) {
        document.getElementById('receipt-number').textContent = receipt;
        
        // Load order details
        const orderData = JSON.parse(localStorage.getItem('currentOrder'));
        if (orderData) {
            document.getElementById('order-number').textContent = 'ORD-' + Date.now();
            document.getElementById('order-amount').textContent = formatPrice(orderData.total);
        }
    }
    
    if (code) {
        document.getElementById('error-code').textContent = code;
    }
}

// Retry failed payment
function retryPayment() {
    const orderData = JSON.parse(localStorage.getItem('currentOrder'));
    if (orderData) {
        window.location.href = '/payment/mpesa';
    } else {
        window.location.href = '/cart/view';
    }
}
