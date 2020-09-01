document.addEventListener('DOMContentLoaded', function() {

    limitListingTitleChars();
});

function limitListingTitleChars() {
    document.querySelectorAll('.listing-title').forEach(function(listingTitle) {
        var listingTitleChars = listingTitle.innerHTML;

        if (listingTitleChars.length >= 17) {
            var limitedListingTitle = listingTitleChars.substring(0, 17);
            limitedListingTitle += "...";
            listingTitle.innerHTML = limitedListingTitle;
        }
    });

}
