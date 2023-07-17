$(function(){

    // 거래내역 조회 (GET 요청)
    $('#query_transaction').on('click', function(){
        $.ajax({
            url: '/transactions',
            type: 'get',
            dataType: 'json',
            success: function(response){
                console.log(response.transactions)
                console.log(response.length)
            },
            error: function(error){
                console.log('에러가 발생 했어요 ㅠㅠ', error)
            },
        });
    });


    // 거래내역 추가 (POST 요청)
    $('#submit-btn').on('click', function(e){
        e.preventDefault()
        let send_data = {
            'send_blockchain_addr': $('#send_blockchain_addr').val(),
            'recv_blockchain_addr': $('#recv_blockchain_addr').val(),
            'amount': $('#amount').val(),
        }
        $.ajax({
            url: '/transactions',
            type: 'put',
            data: JSON.stringify(send_data),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response){
                if (response.status === 'success'){
                    alert('거래 추가 성공!')
                }
            },
            error: function(error){
                alert('에러가 발생했어요 ㅠㅠ', error)
            }
        })
    });
});