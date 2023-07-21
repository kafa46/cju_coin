from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
)
from mining.utils.blockchain_utils import get_blockchain
from mining.transfer import Transfer

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def home():
    '''Mining 메인화면'''
    return render_template(
        'index.html'
    )

@bp.route('/get_chain/', methods=['GET'])
def get_chain():
    block_chain = get_blockchain()
    response = {
        'chain': block_chain.get('chain')
    }
    return jsonify(response), 200


@bp.route('/transactions/', methods=['GET', 'POST'])
def transactions():
    '''Transaction.transaction_pool 정보를 읽어서 리턴'''
    block_chain = get_blockchain()
    if request.method == 'GET':
        print('Transaction 정보 제공')
        resp = {
            'transactions': block_chain.get('transaction_pool'),
            'length': len(block_chain.get('transaction_pool'))
        }
        return jsonify(resp), 200

    if request.method == 'POST':
        '''transaction 추가'''
        print('블록체인 노드: transaction 추가')
        request_json = request.json
        transfer =  Transfer(
            send_blockchain_addr = request_json.get('send_blockchain_addr'),
            recv_blockchain_addr = request_json.get('recv_blockchain_addr'),
            amount = request_json.get('amount')
        )
        is_transacted = transfer.add_transaction()
        
        if not is_transacted:
            return jsonify({'status': 'fail'})
        return jsonify({'status': 'success'})
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
