document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.order-subtotal').forEach(function(order) {
        loadOrderSubtotal(order.id);
    });

    limitListingTitle();
    loadTotalPrice();
});

function loadOrderSubtotal(orderId) {
    const parsedOrderId = orderId.split("-").pop().trim();
    const orderQuantity = parseInt(document.querySelector(
        `#order-quantity-${parsedOrderId}`).innerHTML);
     const orderPrice = parseFloat(parseOrderPrice(parsedOrderId));
     const orderSubtotal = parseFloat(orderPrice * orderQuantity).toFixed(2);
     document.querySelector(
         `#order-subtotal-${parsedOrderId}`).innerHTML = `$${orderSubtotal}`;
}

function parseOrderPrice(orderId) {
    const orderPrice = document.querySelector(
        `#order-price-${orderId}`).innerHTML;
    const parsedOrderPrice = orderPrice.substring(1, orderPrice.length);
    return parsedOrderPrice;
}

function loadTotalPrice() {
    var totalPrice = 0.00;

    document.querySelectorAll('.order-subtotal').forEach(
        function(order) {
            const parsedOrderSubtotal = parseOrderSubtotal(order.id);
            totalPrice += parseFloat(parsedOrderSubtotal);
    });

    totalPrice = parseFloat(totalPrice).toFixed(2);
    document.querySelector('#total-price').innerHTML = `$${totalPrice}`;
}

function parseOrderSubtotal(orderSubtotalId) {
    const parsedOrderSubtotalId = orderSubtotalId.split("-").pop().trim();
    const orderSubtotal = document.querySelector(
        `#order-subtotal-${parsedOrderSubtotalId}`).innerHTML
    const parsedOrderSubtotal = orderSubtotal.substring(
        1, orderSubtotal.length);
    return parsedOrderSubtotal;
}

function limitListingTitle() {
    document.querySelectorAll('.listing-title').forEach(
        function(listingDesrcParagraph) {
            if (listingDesrcParagraph.innerHTML.length >= 30) {
                var limitedDesrcParagraph = listingDesrcParagraph
                    .innerHTML.substring(0, 30);
                limitedDesrcParagraph += "...";
                listingDesrcParagraph.innerHTML = limitedDesrcParagraph;
            }
    });
}

function toggleBankTransferForm() {
    document.querySelector('#bank-transfer').style.display = "block";
    document.querySelector('#credit-debit').style.display = "none";
}

function toggleCreditDebitForm() {
    document.querySelector('#bank-transfer').style.display = "none";
    document.querySelector('#credit-debit').style.display = "block";
}
