document.addEventListener('DOMContentLoaded', function() {
    limitListingTitleChars();
    loadListingRatingStarsForTrending();
    loadListingRatingStarsForTopProducts();
    loadListingRatingStarsForAllProducts();
});

function limitListingTitleChars() {
    document.querySelectorAll('.listing-title').forEach(
        function(listingTitle) {
            var listingTitleChars = listingTitle.innerHTML;

            if (listingTitleChars.length >= 15) {
                var limitedListingTitle = listingTitleChars.substring(0, 15);
                limitedListingTitle += "...";
                listingTitle.innerHTML = limitedListingTitle;
        }
    });

}

function loadListingRatingStarsForTrending() {
    document.querySelectorAll('.listing-rating-star-section').forEach(
        function(listingRatingStarSection) {
            var listingId = listingRatingStarSection.dataset.listingid;

            var ratingScoreSection = document.querySelector(
                    `#trending-${listingId}-rating-stars`);

            if (ratingScoreSection != null) {
                var rating_score = listingRatingStarSection
                        .dataset.ratingscore;

                var i;
                var innerHTMLContent = " ";
                for (i = 1; i <= rating_score; i++) {
                    innerHTMLContent += (('<i class="fa fa-star"')
                            + (' style="color: #42f5c2;"></i>'));
                }

                if ((rating_score * 10) % 10 >= 5) {
                    innerHTMLContent += (('<i class="fa fa-star-half"')
                            + (' style="color: #42f5c2;"></i>'));
                }

                ratingScoreSection.innerHTML = innerHTMLContent;
            }
    });
}

function loadListingRatingStarsForTopProducts() {
    document.querySelectorAll('.listing-rating-star-section').forEach(
        function(listingRatingStarSection) {
            var listingId = listingRatingStarSection.dataset.listingid;

            var ratingScoreSection = document.querySelector(
                    `#topproducts-${listingId}-rating-stars`);

            if (ratingScoreSection != null) {
                var rating_score = listingRatingStarSection
                        .dataset.ratingscore;

                var i;
                var innerHTMLContent = " ";
                for (i = 1; i <= rating_score; i++) {
                    innerHTMLContent += (('<i class="fa fa-star"')
                            + (' style="color: #42f5c2;"></i>'));
                }

                if ((rating_score * 10) % 10 >= 5) {
                    innerHTMLContent += (('<i class="fa fa-star-half"')
                            + (' style="color: #42f5c2;"></i>'));
                }

                ratingScoreSection.innerHTML = innerHTMLContent;
            }
    });
}

function loadListingRatingStarsForAllProducts() {
    document.querySelectorAll('.listing-rating-star-section').forEach(
        function(listingRatingStarSection) {
            var listingId = listingRatingStarSection.dataset.listingid;

            var ratingScoreSection = document.querySelector(
                    `#allproducts-${listingId}-rating-stars`);

            if (ratingScoreSection != null) {
                var rating_score = listingRatingStarSection
                        .dataset.ratingscore;

                var i;
                var innerHTMLContent = " ";
                for (i = 1; i <= rating_score; i++) {
                    innerHTMLContent += (('<i class="fa fa-star"')
                            + (' style="color: #42f5c2;"></i>'));
                }

                if ((rating_score * 10) % 10 >= 5) {
                    innerHTMLContent += (('<i class="fa fa-star-half"')
                            + (' style="color: #42f5c2;"></i>'));
                }

                ratingScoreSection.innerHTML = innerHTMLContent;
            }
    });
}
