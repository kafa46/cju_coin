// my_wallet.html에 진입하거나 
// '새로고침' 클릭했을 경우 코인 수량을 업데이트
$(function(){
    renew_my_wallet();
    $('#renew').on('click', function(){
        // 코인을 조회해서 가져오기
        // get_coin_amount(blockchain_addr);
        renew_my_wallet();
    });
});

function renew_my_wallet(){
    let blockchain_addr = $('#my_blockchain_addr').text();
    get_coin_amount(blockchain_addr);
}

function get_coin_amount(blockchain_addr){
    let send_data = {
        'blockchain_addr': blockchain_addr
    }
    $.ajax({
        url: "/get_coin_amount",
        type: 'get',
        data: send_data,
        dataType: 'json',
        success: function(response){
            if (response.status == 'success'){
                $('#my_wallet_current_amount').text(response.amount)
                return parseFloat(response.amount)
            }
        }, 
        error: function(response, status, error){
            // alert('에러가 발생했어요 ㅠㅠ');
            console.log(`status code: ${status}`)
            console.log(`Error: ${error}`)
        }
    })
}