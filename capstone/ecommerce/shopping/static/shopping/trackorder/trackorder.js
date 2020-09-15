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

function updateOrderStatus(button_id) {
    const order_id = parseButtonId(button_id);
    const updated_order_status = 'Completed';

    fetch(`/shopping/updateorder/${order_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            status: updated_order_status
        })
    });

    document.querySelector(`#order-status-${order_id}`).innerHTML =
        `Order Status: <strong>${updated_order_status}</strong>`;
}
