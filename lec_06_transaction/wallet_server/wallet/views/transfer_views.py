from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)
from wallet.forms import TransferForm

bp = Blueprint('transfer', __name__, url_prefix='/')

@bp.route('/transfer/', methods=['GET', 'POST'])
def transfer():
    '''코인 지갑 화면'''
    form = TransferForm()
    
    if request.method=='POST' and form.validate_on_submit():
        data_dic = request.form.to_dict()
        print(f'data_dic: {data_dic}')
        
        # 처리 -> Todo
        # 잔액 확인 수행
        
        # Singnature 생성
        signature = ''
        
        # 보낼 정보 만들어서 blockchain node에게 전송
        json_data = {
            'send_public_key': '',
            'send_blockchain_addr': '',
            'recv_blockchain_addr': '',
            'amount': 10,
            'signature': signature,
        }
        
        result = {
            'status': 'fail',
            'amount': 'not_enough'
        }
        return jsonify(result)
    
    
    return render_template(
        'transfer.html',
        form=form,
    )