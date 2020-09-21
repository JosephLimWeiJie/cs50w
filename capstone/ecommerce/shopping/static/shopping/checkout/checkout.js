document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.order-subtotal').forEach(function(order) {
        loadOrderSubtotal(order.id);
    });

    limitListingTitle();
    loadTotalPrice();
});

function loadOrderSubtotal(orderId) {
    const PARSED_ORDER_ID = orderId.split("-").pop().trim();
    const ORDER_QUANTITY = parseInt(document.querySelector(
        `#order-quantity-${PARSED_ORDER_ID}`).innerHTML);
     const ORDER_PRICE = parseFloat(parseOrderPrice(PARSED_ORDER_ID));
     const ORDER_SUBTOTAL = parseFloat(ORDER_PRICE * ORDER_QUANTITY).toFixed(2);
     document.querySelector(
         `#order-subtotal-${PARSED_ORDER_ID}`).innerHTML = `$${ORDER_SUBTOTAL}`;
}

function parseOrderPrice(orderId) {
    const ORDER_PRICE = document.querySelector(
        `#order-price-${orderId}`).innerHTML;
    const PARSED_ORDER_PRICE = ORDER_PRICE.substring(1, ORDER_PRICE.length);
    return PARSED_ORDER_PRICE;
}

function loadTotalPrice() {
    var totalPrice = 0.00;

    document.querySelectorAll('.order-subtotal').forEach(
        function(order) {
            const PARSED_ORDER_SUBTOTAL = parseOrderSubtotal(order.id);
            totalPrice += parseFloat(PARSED_ORDER_SUBTOTAL);
    });

    totalPrice = parseFloat(totalPrice).toFixed(2);
    document.querySelector('#total-price').innerHTML = `$${totalPrice}`;
}

function parseOrderSubtotal(orderSubtotalId) {
    const PARSED_ORDER_SUBTOTAL_ID = orderSubtotalId.split("-").pop().trim();
    const ORDER_SUBTOTAL = document.querySelector(
        `#order-subtotal-${PARSED_ORDER_SUBTOTAL_ID}`).innerHTML
    const PARSED_ORDER_SUBTOTAL = ORDER_SUBTOTAL.substring(
        1, ORDER_SUBTOTAL.length);
    return PARSED_ORDER_SUBTOTAL;
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
