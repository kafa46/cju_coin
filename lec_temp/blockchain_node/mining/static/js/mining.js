$(function(){
    // 코인 amount 요청
    $('#query_coin_status').on('click', function(){
        reload_amount();
    });
});

// 코인 amount 자동 요청
function reload_amount(){
    let blockchain_addr = $('#blockchain_addr_input').val()
    let send_data = {'blockchain_addr': blockchain_addr}
    $.ajax({
        url: "/coin_amount",
        type: 'post',
        data: JSON.stringify(send_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(response){
            if (response.status == 'success'){
                console.log(response.content)
                $('#current_coin_amount').val(response.content)
            }
        },
        error: function(error){
            console.log('에러가 발생했어요 ㅠㅠ', error)
        }
    });
}

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