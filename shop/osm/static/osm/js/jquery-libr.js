$(document).ready(function() {

    var width;
    var animationSpeed = 700;
    var currentSlide = 5;

    var wid = $('#p_slider').width();
    width = wid / 5;
    $('.p_slide').width(width);
    var $slider = $('#p_slides');
    var len;

    $('#next_bt').click(function () {
        var $slides = $(this).parent().parent().find('.p_slide');
        len = $slides.length;
        if (len == currentSlide) {
            $(this).hide();
            $('#prev_bt').show();
        }
        else {
            $('#prev_bt').show();
            $slider.animate({'margin-left': '-=' + width}, animationSpeed);
            if (len == currentSlide) {
                $(this).hide();
                $('#prev_bt').show();
            }
            ++currentSlide;
        }
    });
    $('#prev_bt').click(function () {
        if (currentSlide == 5) {
            $(this).hide();
            $('#next_bt').show();
        }
        else {
            $('#next_bt').show();
            $slider.animate({'margin-left': '+=' + width}, animationSpeed);
            if (currentSlide == 5) {
                $(this).hide();
                $('#next_bt').show();
            }
            --currentSlide;
        }
    });
});