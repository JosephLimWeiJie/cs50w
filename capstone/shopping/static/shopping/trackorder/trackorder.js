document.addEventListener('DOMContentLoaded', function() {
    limitListingDesrc();
    loadReceiveButton();
});

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

function loadReceiveButton() {
    document.querySelectorAll('.receive-btn').forEach(function(button) {
        button.addEventListener(
            'click', () => updateOrderStatus(button.id));
    });
}

function updateOrderStatus(buttonId) {
    const ORDER_ID = parseButtonId(buttonId);
    const UPDATED_ORDER_STATUS = 'Completed';

    fetch(`/shopping/updateorder/${ORDER_ID}`, {
        method: 'PUT',
        body: JSON.stringify({
            status: UPDATED_ORDER_STATUS
        })
    });

    document.querySelector(`#order-status-${order_id}`).innerHTML =
        `Order Status: <strong>${updated_order_status}</strong>`;
}
