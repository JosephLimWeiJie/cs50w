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

    loadProfilePage();
    loadImageFileName();
    loadCreateNewListingBtn();
    limitListingDesrc();
    loadReviewRating();
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
    const updated_email = document.querySelector('#id_email').value;
    const updated_gender = document.querySelector('#id_gender').value;
    const updated_phone_number = document.querySelector('#id_phone_number').value;
    const updated_date_of_birth = document.querySelector('#id_date_of_birth').value;

    document.querySelector('#span-email').innerHTML = updated_email;
    document.querySelector('#span-gender').innerHTML = updated_gender;
    document.querySelector('#span-phone-number').innerHTML = updated_phone_number;
    document.querySelector('#span-date-of-birth').innerHTML = updated_date_of_birth;

    fetch(`/shopping/updateprofile/2`, {
        method: 'PUT',
        body: JSON.stringify({
            email: updated_email,
            gender: updated_gender,
            phone_number: updated_phone_number,
            date_of_birth: updated_date_of_birth
        })
    });

    loadMyAccount();
    return false;
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
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });
}

function loadCreateNewListingBtn() {
    $('#listingModal').on('shown.bs.modal', function () {
      $('#myInput').trigger('focus')
  });
}

function limitListingDesrc() {
    const listingDesrcParagraph = document.querySelector('.listing-desrc');
    if (listingDesrcParagraph.innerHTML.length >= 30) {
        var limitedDesrcParagraph = listingDesrcParagraph.innerHTML.substring(0, 30);
        limitedDesrcParagraph += "...";
        listingDesrcParagraph.innerHTML = limitedDesrcParagraph;
    }
}

function loadReviewRating() {
    document.querySelectorAll('.rating-stars').forEach(function(reviewDiv) {
        var ratingValue = reviewDiv.dataset.ratingvalue;

        var i;
        for (i = 1; i <= ratingValue; i++) {
            const spanForStars = document.createElement('span');
            spanForStars.innerHTML = '<i class="fa fa-star">';
            spanForStars.style.color = "#42f5c2";
            reviewDiv.appendChild(spanForStars);
        }
    });
}
