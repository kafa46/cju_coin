// 글자 깜빡이기
$(function(){
    setInterval(function(){
        let opacity = $('.blink').css("opacity");
        if (opacity > 0){
            $('.blink').css('opacity', 0);
        } else if (opacity == 0){
            $('.blink').css('opacity', 1);
        }
    }, 1000);
});