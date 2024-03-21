$(document).ready(function () {
    var hideTimeout;
    $('#eventCarousel').hover(
        function () {
            clearTimeout(hideTimeout);
            $('.carousel-control-prev, .carousel-control-next').css('opacity', '1');
            $('.carousel-item::before, .carousel-item::after').css('opacity', '1');
        },
        function () {
            hideTimeout = setTimeout(function () {
                $('.carousel-control-prev, .carousel-control-next').css('opacity', '0');
                $('.carousel-item::before, .carousel-item::after').css('opacity', '0');
            }, 3000); // 3 seconds timeout
        }
    );
});
