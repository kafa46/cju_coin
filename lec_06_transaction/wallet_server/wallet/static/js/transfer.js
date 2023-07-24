$(function(){
    $('#submit-btn').on('click', function(e){
        e.preventDefault();
        let decision = confirm('정말로 이체하시겠습니까?')
        if (decision == true){
            let send_string = $('#transfer-form').serialize()
            $.ajax({
                url: '/transfer',
                type: 'post',
                data: send_string,
                dataType: 'json',
                success: function(response){
                    if (response.status == 'success'){
                        alert('이체 성공했습니다!');
                        $('#form-area').attr('hidden', true);
                        $('#success-msg').text(`${response.amount} 코인 이체에 성공했습니다.`)
                        $('#after-transfer').attr('hidden', false)

                    }
                    if (response.status == 'fail'){
                        if (response.amount == 'not_enough'){
                            alert(`이체하려는 금액이 잔액보다 커서 보낼수 없습니다.\n이체 수량을 확인해 주세요`)
                        }
                    }

                },
                error: function(error){
                    alert('이체에 실패 했습니다. ㅠㅠ', error)
                }
            })
        }
    });
});