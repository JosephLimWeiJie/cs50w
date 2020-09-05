document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#plus-btn').addEventListener(
        'click', () => plusQuantity());
    document.querySelector('#minus-btn').addEventListener(
        'click', () => minusQuantity());

    limitListingDesrc();
});

function plusQuantity() {
    var currQuantityCount = parseInt(
        document.querySelector('#quantity-count').value);
    const quantityLeft = parseInt(
        document.querySelector('#quantity-count').dataset.quantity);

    if (currQuantityCount === quantityLeft) {
        document.querySelector('#plus-btn').disabled = true;
    } else if (currQuantityCount < quantityLeft) {
        currQuantityCount += 1;
        document.querySelector('#quantity-count').value = currQuantityCount;
        document.querySelector('#minus-btn').disabled = false;
    }

    $(document).ready(function() {
        $('#plus-btn').click(function() {
            $("quantity_count:text").val(currQuantityCount);
        });
    });
}

function minusQuantity() {
    var currQuantityCount = parseInt(
        document.querySelector('#quantity-count').value);

    if (currQuantityCount === 0) {
        document.querySelector('#minus-btn').disabled = true;
    } else if (currQuantityCount > 0) {
        currQuantityCount -= 1;
        document.querySelector('#plus-btn').disabled = false;
        document.querySelector('#quantity-count').value = currQuantityCount;
    }

    $(document).ready(function() {
        $('#minus-btn').click(function() {
            $("quantity_count:text").val(currQuantityCount);
        });
    });
}

function loadTotalPrice() {
    var totalPrice = calculateTotalPrice();
    document.querySelector('#total-price').innerHTML = totalPrice;
}

function calculateTotalPrice() {
    var totalPrice = 0.00;
    document.querySelectorAll(".order-price").forEach(function(order) {
        const orderPrice = parseOrderPrice(order.innerHTML);
        totalPrice += orderPrice;
    });
    return totalPrice;
}

function parseOrderPrice(order) {
    parsedOrderPrice = parseFloat(order.substring(1, order.length));
    return parsedOrderPrice;
}

function limitListingDesrc() {
    document.querySelectorAll('.listing-desrc').forEach(
        function(listingDesrcParagraph) {
            if (listingDesrcParagraph.innerHTML.length >= 30) {
                var limitedDesrcParagraph = listingDesrcParagraph
                    .innerHTML.substring(0, 30);
                limitedDesrcParagraph += "...";
                listingDesrcParagraph.innerHTML = limitedDesrcParagraph;
            }
    });
}
