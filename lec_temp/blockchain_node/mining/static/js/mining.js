var start_coin_amount = 0;
var current_coin_amount = 0;
var mining_reward = 0;

$(function(){

    // 코인 amount 요청
    $('#query_coin_status').on('click', function(){
        reload_amount();
    });

    // 채굴 시작
    $('#mining_start').on('click', function(e){
        let decision = confirm('채굴하는 동안에는 컴퓨터가 항상 켜져 있어야 합니다 ^^. \n채굴을 시작할까요?')
        if (decision==false){
            return false
        }
        $('#msg_for_start_mining').attr('hidden', false);
        $('#mining_reward_area').attr('hidden', false);
        $('#msg_for_stop_mining').attr('hidden', true);
        $('#msg_for_stopping_completed').attr('hidden', true);
        $('#mining_stop').attr('hidden', false)
        $('#mining_start').attr('hidden', true)

        //코인 amount 자동 업데이트
        setInterval(reload_amount, 3000);

        mining_reward = 0;
        start_coin_amount = current_coin_amount;

        // 채굴 시작할때 보유 코인 display
        $('#mining_coin_status').attr('hidden', false)
        $('#coin_amount_at_start').attr('hiiden', false)
        $('#coin_amount_at_start').text(current_coin_amount)

        // 채굴보상금 display
        $('#mining_coin_status').val('hidden', false);
        $('#mining_coin_status').val(mining_reward);

        let blockchain_addr = $('#blockchain_addr_input').val();

        let send_data = {'blockchain_addr': blockchain_addr}
        $.ajax({
            url: '/mining/start',
            type: 'post',
            data: JSON.stringify(send_data),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response){
                if (response.status == 'success'){
                    console.log('Success to start mining.')
                }
                if (response.status == 'fail'){
                    alert(response.reason)
                }
            },
            error: function(error){
                console.log('에러가 발생했어요 ㅠㅠ', error)
            }
        });
    });

    // 채굴 중단
    $('#mining_stop').on('click', function(){
        let decision = confirm('채굴을 중단할까요?')
        if (decision==false){return false}
        $('#msg_for_start_mining').attr('hidden', true)
        $('#msg_for_stop_mining').attr('hidden', false)
        $.ajax({
            url: '/mining/stop',
            type: 'post',
            data: JSON.stringify({'stop_flag': 'stop'}),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response){
                if (response.status == 'stopped'){
                    $('#msg_for_stopping_completed').attr('hidden', false)
                    $('#mining_start').attr('hidden', false)
                    $('#mining_stop').attr('hidden', true)
                }
            },
            error: function(error){
                console.log('에러가 발생했어요 ㅠㅠ', error)
            }
        });
    })
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
                current_coin_amount = response.content;
                if (start_coin_amount == 0){
                    start_coin_amount = response.content;
                }
                mining_reward = parseInt(current_coin_amount) - start_coin_amount;
                $('#current_coin_amount').val(response.content)
                $('#mining_reward_amount').val(mining_reward)
            }
        },
        error: function(error){
            console.log('에러가 발생했어요 ㅠㅠ', error)
        }
    });
}

// 글자 깜빡이기
$(function(){
    setInterval(function () {
        var opacity = $('.blink').css("opacity");
        if (opacity > 0) {
          $(".blink").css("opacity", 0);
        }
        else if (opacity == 0) {
          $(".blink").css("opacity", 1);
        }
    }, 1000);
});