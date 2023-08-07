// 전역변수 지정
var start_coin_amount = 0;
var current_coin_amount = 0;
var mining_reward = 0;

$(function(){
    // 코인 amount 요청
    $('#query_coin_status').on('click', function(){
        reload_amount();
    });
    $('#miner_wallet_addr').on('change', function(){
        reload_amount();
    });

    // 채굴 시작
    $('#mining_start').on('click', function(){
        let decision = confirm('채굴하는 동안에는 컴퓨터가 항상 켜져 있어야 합니다.\n채굴을 시작할까요?')
        if (decision == false){
            return false;
        }
        // 채굴자 주소가 입력되어 있는지 확인
        let blockchain_addr = $('#blockchain_addr_input').val()
        if (blockchain_addr==''){
            alert('채굴자 지갑 수소를 입력하셔야 합니다.')
            return false
        }
        // 채굴자가 코인을 조회했는지 검사
        if ($('#current_coin_amount').val()==''){
            alert('채굴을 시작하려면 코인 현황을 먼저 조회해야 합니다.')
            return false
        }

        // 채굴 중단 버튼 보이기
        $('#mining_stop').attr('hidden', false)
        // 채굴 시작 버튼 숨기기
        $('#mining_start').attr('hidden', true)
        // 채굴시작 안내하는 메시지 보이기
        $('#msg_for_start_mining').attr('hidden', false)
        // 채굴 보상금 보이기
        $('#mining_reward_area').attr('hidden', false)
        // 채굴 중단 버튼을 클릭했을 때 보여줄 메시지 숨김
        $('#msg_for_stop_mining').attr('hidden', true)
        // 채굴이 완전히 중단되었을 때 보여줄 메시지 숨김
        $('#msg_for_stopping_completed').attr('hidden', true)

        // 코인 amount 업데이트
        if ($('#current_coin_amount').val() == ''){
            alert('코인 조회를 마친 이후에 채굴을 시작할 수 있습니다.')
            return false
        }
        reload_amount();
        current_coin_amount = $('#current_coin_amount').val();
        start_coin_amount = current_coin_amount;
        // 코인 amount 자동 업데이트 시간 설정
        setInterval(reload_amount, 3000)

        // 시작할때 보유한 코인 기록
        $('#mining_coin_status').attr('hidden', false)
        $('#coin_amount_at_start').text(start_coin_amount)

        let send_data = {'blockchain_addr': blockchain_addr};
        $.ajax({
            url: '/mining/start', 
            type: 'post',
            data: JSON.stringify(send_data),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response){
                if (response.status == 'success'){
                    reload_amount();
                }
                if (response.status == 'fail'){
                    console.log(response.reason)
                }
            },
            error: function(error){
                console.log(error)
            }
        });
    });

    // 채굴 중단
    $('#mining_stop').on('click', function(){
        let decision = confirm('채굴을 중단할까요?')
        if (decision==false){return false}
        $('#msg_for_start_mining').attr('hidden', true)
        $('#msg_for_stop_mining').attr('hidden', false)
        $('#mining_stop').attr('hidden', true)
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
            error: function(response, status_code, error){
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
                current_coin_amount = response.content
                if (start_coin_amount == 0){
                    start_coin_amount = response.content
                }
                // 현재 코인 현황 업데이트
                $('#current_coin_amount').val(current_coin_amount)
                // 채굴 보상금 업데이트
                mining_reward = parseFloat(current_coin_amount) - parseFloat(start_coin_amount);
                $('#mining_reward_amount').val(mining_reward);
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
