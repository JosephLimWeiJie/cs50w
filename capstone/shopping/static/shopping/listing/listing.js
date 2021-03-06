document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#plus-btn').addEventListener(
        'click', () => plusQuantity());
    document.querySelector('#minus-btn').addEventListener(
        'click', () => minusQuantity());

    updateListingClickRate();

    loadImageCarousel();
    loadRatingFormWidget();
    loadReviewRating();
    loadEditRatingFormWidget();
    loadListingRatingStars();
});

function loadImageCarousel() {
    const IMAGE_COUNT = document.querySelector('#imagesCount').innerHTML;

    var i;
    for (i = 1; i < IMAGE_COUNT; i++) {
        var newLiElement = document.createElement('li');
        newLiElement.dataset.target = "#listingImageIndicators";
        newLiElement.dataset.slide = i;

        document.querySelector(
                '#carouselIndicators').appendChild(newLiElement);
    }
}

function plusQuantity() {
    var currQuantityCount = parseInt(
        document.querySelector('#quantity-count').value);
    const QUANTITY_LEFT = parseInt(
        document.querySelector('#quantity-count').dataset.quantity);

    if (currQuantityCount === QUANTITY_LEFT) {
        document.querySelector('#plus-btn').disabled = true;
        return;
    } else if (currQuantityCount < QUANTITY_LEFT) {
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

    if (currQuantityCount === 1) {
        document.querySelector('#minus-btn').disabled = true;
        return;
    } else if (currQuantityCount > 1) {
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

function loadRatingFormWidget() {
    document.querySelector('#rating1').addEventListener(
        'click', () => setRatingValue(1));
    document.querySelector('#rating2').addEventListener(
        'click', () => setRatingValue(2));
    document.querySelector('#rating3').addEventListener(
        'click', () => setRatingValue(3));
    document.querySelector('#rating4').addEventListener(
        'click', () => setRatingValue(4));
    document.querySelector('#rating5').addEventListener(
        'click', () => setRatingValue(5));
}

function setRatingValue(value) {
    document.querySelector('#rating-form-input').value = value;

    // Reset all the stars color to black.
    var i;
    for (i = 1; i <= 5; i++) {
        document.querySelector(`#rating${i}`).style.color = "black";
    }

    // Set stars' color to respective values.
    var j;
    for (j = 1; j <= value; j++) {
        document.querySelector(`#rating${j}`).style.color = "#42f5c2";
    }
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

function loadEditRatingFormWidget() {
    document.querySelector('#newrating1').addEventListener(
        'click', () => setNewRatingValue(1));
    document.querySelector('#newrating2').addEventListener(
        'click', () => setNewRatingValue(2));
    document.querySelector('#newrating3').addEventListener(
        'click', () => setNewRatingValue(3));
    document.querySelector('#newrating4').addEventListener(
        'click', () => setNewRatingValue(4));
    document.querySelector('#newrating5').addEventListener(
        'click', () => setNewRatingValue(5));
}

function setNewRatingValue(value) {
    document.querySelector('#edited-rating-form-input').value = value;

    // Reset all the stars color to black.
    var i;
    for (i = 1; i <= 5; i++) {
        document.querySelector(`#newrating${i}`).style.color = "black";
    }

    // Set stars' color to respective values.
    var j;
    for (j = 1; j <= value; j++) {
        document.querySelector(`#newrating${j}`).style.color = "#42f5c2";
    }
}

function loadListingRatingStars() {
    const LISTING_RATING_SECTION = document.querySelector(
            '#listing-rating-section');
    var rating_score = LISTING_RATING_SECTION.dataset.ratingscore;

    var i;
    var innerHTMLContent = " "
    for (i = 1; i <= rating_score; i++) {
        innerHTMLContent += (
                '<i class="fa fa-star"'
                + ' style="color: #42f5c2;"></i>');
    }

    if ((rating_score * 10) % 10 >= 5) {
        innerHTMLContent += (
                '<i class="fa fa-star-half"'
                + ' style="color: #42f5c2;"></i>');
    }

    LISTING_RATING_SECTION.innerHTML = innerHTMLContent;
}

function updateListingClickRate() {
    const LISTING_ID = parseInt(
            document.querySelector('#main-listing-id').innerHTML);
    const CURR_CLICK_RATE = parseInt(
            document.querySelector('#main-listing-click-rate').innerHTML);
    const UPDATED_CLICK_RATE = CURR_CLICK_RATE + 1;

    fetch(`/shopping/updatelisting/${LISTING_ID}`, {
        method: 'PUT',
        body: JSON.stringify({
            click_rate: UPDATED_CLICK_RATE
        })
    });
}
