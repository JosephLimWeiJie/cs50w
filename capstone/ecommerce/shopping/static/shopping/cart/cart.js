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

function plusQuantity(button_id) {
    const button_id_number = button_id.split("-").pop().trim();

    var currQuantityCount = parseInt(
        document.querySelector(`#quantity-count-${button_id_number}`).value);
    const quantityLeft = parseInt(
        document.querySelector(`#quantity-count-${button_id_number}`).dataset.quantity);

    if (currQuantityCount === quantityLeft) {
        document.querySelector(`#plus-btn-${button_id_number}`).disabled = true;
        return;
    } else if (currQuantityCount < quantityLeft) {
        currQuantityCount += 1;
        document.querySelector(`#quantity-count-${button_id_number}`).value = currQuantityCount;
        document.querySelector(`#minus-btn-${button_id_number}`).disabled = false;
    }

    $(document).ready(function() {
        $(`#plus-btn-${button_id_number}`).click(function() {
            $("quantity_count:text").val(currQuantityCount);
        });
    });

    updateOrder(button_id_number);
    updateTotalPrice(button_id_number, "plus");
}

function minusQuantity(button_id) {
    const button_id_number = button_id.split("-").pop().trim();

    var currQuantityCount = parseInt(
        document.querySelector(`#quantity-count-${button_id_number}`).value);
    if (currQuantityCount === 1) {
        document.querySelector(`#minus-btn-${button_id_number}`).disabled = true;
        return;
    } else if (currQuantityCount > 0) {
        currQuantityCount -= 1;
        document.querySelector(`#plus-btn-${button_id_number}`).disabled = false;
        document.querySelector(`#quantity-count-${button_id_number}`).value = currQuantityCount;
    }

    $(document).ready(function() {
        $(`#minus-btn-${button_id_number}`).click(function() {
            $("quantity_count:text").val(currQuantityCount);
        });
    });

    updateOrder(button_id_number);
    updateTotalPrice(button_id_number, "minus");
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

function updateOrder(order_id) {
    const updated_quantity_demanded = parseInt(document.querySelector(
        `#quantity-count-${order_id}`).value);

    fetch(`/shopping/updateorder/${order_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            "quantity_demanded": updated_quantity_demanded
        })
    });

    return false;
}

function updateTotalPrice(order_id, command) {
    var parsedOrderPrice = parseOrderPrice(order_id);
    var currTotalPrice = parseTotalPrice();
    var updatedTotalPrice;

    if (command === "plus") {
        updatedTotalPrice = parseFloat(currTotalPrice) + parseFloat(parsedOrderPrice);
    } else if (command === "minus") {
        updatedTotalPrice = parseFloat(currTotalPrice) - parseFloat(parsedOrderPrice);
    }

    updatedTotalPrice = parseFloat(updatedTotalPrice).toFixed(2);
    document.querySelector('#total-price').innerHTML = `$${updatedTotalPrice}`;
}

function parseOrderPrice(order_id) {
    const orderPrice = document.querySelector(`#order-price-${order_id}`).innerHTML;
    const parsedOrderPrice = orderPrice.substring(1, orderPrice.length);
    return parsedOrderPrice;
}

function parseTotalPrice() {
    const currTotalPrice = document.querySelector('#total-price').innerHTML;
    const parsedCurrTotalPrice = currTotalPrice.substring(1, currTotalPrice.length);
    return parsedCurrTotalPrice;
}
