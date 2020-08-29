document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#plus-btn').addEventListener(
        'click', () => plusQuantity());
    document.querySelector('#minus-btn').addEventListener(
        'click', () => minusQuantity());

    loadImageCarousel();
});

function loadImageCarousel() {
    const imageCount = document.querySelector('#imagesCount').innerHTML;

    var i;
    for (i = 1; i <= imageCount; i++) {
        var newLiElement = document.createElement('li');
        newLiElement.dataset.target = "#listingImageIndicators";
        newLiElement.dataset.slide = i;

        document.querySelector('#carouselIndicators').appendChild(newLiElement);
    }
}

function plusQuantity() {
    var currQuantityCount = parseInt(document.querySelector('#quantity-count').value);
    const quantityLeft = parseInt(document.querySelector('#quantity-count').dataset.quantity);

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
    var currQuantityCount = parseInt(document.querySelector('#quantity-count').value);

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
