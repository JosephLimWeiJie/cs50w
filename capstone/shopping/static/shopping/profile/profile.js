document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#my-account-btn').addEventListener(
        'click', () => loadMyAccount());
    document.querySelector('#my-purchase-btn').addEventListener(
        'click', () => loadMyPurchase());
    document.querySelector('#my-shop-btn').addEventListener(
        'click', () => loadMyShop());
    document.querySelector('#notif-btn').addEventListener(
        'click', () => loadNotif());
    document.querySelector('#edit-profile-btn').addEventListener(
        'click', () => loadEditForm());
    document.querySelector('#undo-btn').addEventListener(
        'click', () => loadMyAccount());
    document.querySelector('#edit-profile-form').onsubmit =
        updateMyAccount;
    document.querySelector('#create-listing-btn').addEventListener(
        'submit', () => createNewListingNotification());

    loadProfilePage();
    loadImageFileName();
    loadCreateNewListingBtn();
    limitListingDesrc();
    loadReviewRating();
    loadUpdateOrderStatus();
});

function loadProfilePage() {
    document.querySelector('#my-account').style.display = "block";
    document.querySelector('#my-purchase').style.display = "none";
    document.querySelector('#my-shop').style.display = "none";
    document.querySelector('#notif').style.display = "none";
    document.querySelector('#edit').style.display = "none";
}

function loadMyAccount() {
    document.querySelector('#my-account').style.display = "block";
    document.querySelector('#my-purchase').style.display = "none";
    document.querySelector('#my-shop').style.display = "none";
    document.querySelector('#notif').style.display = "none";
    document.querySelector('#edit').style.display = "none";
}

function loadMyPurchase() {
    document.querySelector('#my-account').style.display = "none";
    document.querySelector('#my-purchase').style.display = "block";
    document.querySelector('#my-shop').style.display = "none";
    document.querySelector('#notif').style.display = "none";
    document.querySelector('#edit').style.display = "none";

    limitListingDesrc();
}

function loadMyShop() {
    document.querySelector('#my-account').style.display = "none";
    document.querySelector('#my-purchase').style.display = "none";
    document.querySelector('#my-shop').style.display = "block";
    document.querySelector('#notif').style.display = "none";
    document.querySelector('#edit').style.display = "none";
}

function loadNotif() {
    document.querySelector('#my-account').style.display = "none";
    document.querySelector('#my-purchase').style.display = "none";
    document.querySelector('#my-shop').style.display = "none";
    document.querySelector('#notif').style.display = "block";
    document.querySelector('#edit').style.display = "none";
}

function loadEditForm() {
    document.querySelector('#my-account').style.display = "none";
    document.querySelector('#my-purchase').style.display = "none";
    document.querySelector('#my-shop').style.display = "none";
    document.querySelector('#notif').style.display = "none";
    document.querySelector('#edit').style.display = "block";
}

function updateMyAccount() {
    const UPDATED_EMAIL = document.querySelector('#id_email').value;
    const UPDATED_GENDER = document.querySelector('#id_gender').value;
    const UPDATED_PHONE_NUMBER = document.querySelector(
                '#id_phone_number').value;
    const UPDATED_DATE_OF_BIRTH = document.querySelector(
                '#id_date_of_birth').value;

    document.querySelector('#span-email').innerHTML = UPDATED_EMAIL;
    document.querySelector('#span-gender').innerHTML = UPDATED_GENDER;
    document.querySelector('#span-phone-number').innerHTML
            = UPDATED_PHONE_NUMBER;
    document.querySelector('#span-date-of-birth').innerHTML
            = UPDATED_DATE_OF_BIRTH;

    fetch(`/shopping/updateprofile/2`, {
        method: 'PUT',
        body: JSON.stringify({
            email: UPDATED_EMAIL,
            gender: UPDATED_GENDER,
            phone_number: UPDATED_PHONE_NUMBER,
            date_of_birth: UPDATED_DATE_OF_BIRTH
        })
    });

    loadMyAccount();
    return false;
}

function loadUpdateOrderStatus() {
    document.querySelectorAll('.update-order-status-btn').forEach(
        function(button) {
            button.addEventListener(
                'click', () => updateOrderStatus(button.id));
        });
}

function updateOrderStatus(button_id) {
    const order_id = parseButtonId(button_id);
    const updated_order_status = document.querySelector(
            `#select-order-status-${order_id}`).value;

    fetch(`/shopping/updateorder/${order_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            status: updated_order_status
        })
    });

    document.querySelector(`#order-status-${order_id}`).innerHTML =
        `Order Status: <strong>${updated_order_status}</strong>`;
}

function parseButtonId(button_id) {
    const id = button_id.split("-").pop();
    return id;
}

function loadFile(event) {
    var output = document.getElementById('output');
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
    }

    document.querySelector('#profile-pic-btn').style.display = "block";
    document.querySelector('#profile-pic-btn').style.position = "absolute";
    document.querySelector('#profile-pic-btn').style.right = "0";
    document.querySelector('#profile-pic-btn').style.marginTop = "5%";
    document.querySelector('#profile-pic-btn').style.fontSize = "12px";
}

function loadImageFileName() {
    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label")
                .addClass("selected").html(fileName);
    });
}

function loadCreateNewListingBtn() {
    $('#listingModal').on('shown.bs.modal', function () {
      $('#myInput').trigger('focus')
  });
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

function loadReviewRating() {
    document.querySelectorAll('.rating-stars').forEach(function(reviewDiv) {
        var ratingValue = reviewDiv.dataset.ratingvalue;

        var i;
        for (i = 1; i <= ratingValue; i++) {
            const SPAN_FOR_STARS = document.createElement('span');
            SPAN_FOR_STARS.innerHTML = '<i class="fa fa-star">';
            SPAN_FOR_STARS.style.color = "#42f5c2";
            reviewDiv.appendChild(SPAN_FOR_STARS);
        }
    });
}

function createNewListingNotification() {
    alert('You have created a new listing.');
}
