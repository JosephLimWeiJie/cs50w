document.addEventListener('DOMContentLoaded', function() {
    limitListingDesrc();
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
