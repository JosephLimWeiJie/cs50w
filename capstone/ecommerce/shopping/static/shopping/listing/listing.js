document.addEventListener('DOMContentLoaded', function() {
    loadImageCarousel();
});

function loadImageCarousel() {
    const imageCount = document.querySelector('#imagesCount').innerHTML;

    var i;
    for (i = 1; i <= imageCount; i++) {
        newLiElement = document.createElement('li');
        newLiElement.dataset['target'] = "#listingImageIndicators";
        newLiElement.dataset['slide'] = i;

        document.querySelector('.carousel-indicators').appendChild(newLiElement);
    }
}
