$(document).ready(function () {
    var hideTimeout;
    $('#eventCarousel').hover(
        function () {
            clearTimeout(hideTimeout);
            $('.carousel-control-prev, .carousel-control-next').css('opacity', '1');
        },
        function () {
            hideTimeout = setTimeout(function () {
                $('.carousel-control-prev, .carousel-control-next').css('opacity', '0');
            }, 5000); // Adjust the time (in milliseconds) as needed
        }
    );
});
