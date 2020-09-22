document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.plus-btn').forEach(function(plusBtn) {
        plusBtn.onclick = function() {
            plusQuantity(this.id);
        }
    });
    document.querySelectorAll('.minus-btn').forEach(function(minusBtn) {
        minusBtn.onclick = function() {
            minusQuantity(this.id);
        }
    });

    limitListingDesrc();
});

function plusQuantity(buttonId) {
    const BUTTON_ID_NUMBER = buttonId.split("-").pop().trim();

    var currQuantityCount = parseInt(
        document.querySelector(`#quantity-count-${BUTTON_ID_NUMBER}`).value);
    const quantityLeft = parseInt(
        document.querySelector(
            `#quantity-count-${BUTTON_ID_NUMBER}`).dataset.quantity);

    if (currQuantityCount === quantityLeft) {
        document.querySelector(
            `#plus-btn-${BUTTON_ID_NUMBER}`).disabled = true;
        return;
    } else if (currQuantityCount < quantityLeft) {
        currQuantityCount += 1;
        document.querySelector(
            `#quantity-count-${BUTTON_ID_NUMBER}`).value = currQuantityCount;
        document.querySelector(
            `#minus-btn-${BUTTON_ID_NUMBER}`).disabled = false;
    }

    $(document).ready(function() {
        $(`#plus-btn-${BUTTON_ID_NUMBER}`).click(function() {
            $("quantity_count:text").val(currQuantityCount);
        });
    });

    updateOrder(BUTTON_ID_NUMBER);
    updateTotalPrice(BUTTON_ID_NUMBER, "plus");
}

function minusQuantity(buttonId) {
    const BUTTON_ID_NUMBER = buttonId.split("-").pop().trim();

    var currQuantityCount = parseInt(
        document.querySelector(`#quantity-count-${BUTTON_ID_NUMBER}`).value);
    if (currQuantityCount === 1) {
        document.querySelector(
            `#minus-btn-${BUTTON_ID_NUMBER}`).disabled = true;
        return;
    } else if (currQuantityCount > 0) {
        currQuantityCount -= 1;
        document.querySelector(
            `#plus-btn-${BUTTON_ID_NUMBER}`).disabled = false;
        document.querySelector(
            `#quantity-count-${BUTTON_ID_NUMBER}`).value = currQuantityCount;
    }

    $(document).ready(function() {
        $(`#minus-btn-${BUTTON_ID_NUMBER}`).click(function() {
            $("quantity_count:text").val(currQuantityCount);
        });
    });

    updateOrder(BUTTON_ID_NUMBER);
    updateTotalPrice(BUTTON_ID_NUMBER, "minus");
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

function updateOrder(orderId) {
    const UPDATED_QUANTITY_DEMANDED = parseInt(document.querySelector(
        `#quantity-count-${orderId}`).value);

    fetch(`/shopping/updateorder/${orderId}`, {
        method: 'PUT',
        body: JSON.stringify({
            "quantity_demanded": UPDATED_QUANTITY_DEMANDED
        })
    });

    return false;
}

function updateTotalPrice(orderId, command) {
    var parsedOrderPrice = parseOrderPrice(orderId);
    var currTotalPrice = parseTotalPrice();
    var updatedTotalPrice;

    if (command === "plus") {
        updatedTotalPrice = parseFloat(
            currTotalPrice) + parseFloat(parsedOrderPrice);
    } else if (command === "minus") {
        updatedTotalPrice = parseFloat(
            currTotalPrice) - parseFloat(parsedOrderPrice);
    }

    updatedTotalPrice = parseFloat(updatedTotalPrice).toFixed(2);
    document.querySelector(
        '#total-price').innerHTML = `$${updatedTotalPrice}`;
}

function parseOrderPrice(orderId) {
    const ORDER_PRICE = document.querySelector(
        `#order-price-${orderId}`).innerHTML;
    const PARSED_ORDER_PRICE = ORDER_PRICE.substring(1, ORDER_PRICE.length);
    return PARSED_ORDER_PRICE;
}

function parseTotalPrice() {
    const CURR_TOTAL_PRICE = document.querySelector('#total-price').innerHTML;
    const PARSED_CURR_TOTAL_PRICE = CURR_TOTAL_PRICE.substring(
        1, CURR_TOTAL_PRICE.length);
    return PARSED_CURR_TOTAL_PRICE;
}
