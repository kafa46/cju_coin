from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
)
from mining.utils.blockchain_utils import (
    get_blockchain,
    calculate_total_amount,
)
from mining.transfer import Transfer
from mining.mining import Mine
from mining import config

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def home():
    '''Mining 메인화면'''
    return render_template(
        # 'index.html'
        'mining.html',
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
            send_public_key = request_json.get('send_public_key'),
            send_blockchain_addr = request_json.get('send_blockchain_addr'),
            recv_blockchain_addr = request_json.get('recv_blockchain_addr'),
            amount = float(request_json.get('amount')),
            signature = request_json.get('signature')
        )
        is_transacted = transfer.add_transaction()
        
        if not is_transacted:
            return jsonify({'status': 'fail'}), 400
        
        return jsonify({'status': 'success'}), 201
    

@bp.route('/coin_amount/', methods=['GET', 'POST'])
def coin_amount():
    '''코인 갯수를 계산하여 json 리턴'''
    json_data = request.json
    blockchain_addr = json_data['blockchain_addr']
    print(blockchain_addr)
    if not blockchain_addr:
        return jsonify({
            'status': 'fail',
            'content': '지갑주소(blockchain address)가 없습니다.'
        }), 400
    return jsonify({
        'status': 'succcess',
        'content': calculate_total_amount(blockchain_addr)
    }), 201
        

@bp.route('/mining/', methods=['GET', 'POST'])
def mining():
    '''채굴 실행'''
    recv_blockchain_addr = request.args.get('blockchain_addr')
    print(recv_blockchain_addr)
    mine = Mine()
    mining_success, _ = mine.mining(recv_blockchain_addr)
    if mining_success:
        return jsonify({
            'status': 'success',
            'reward': config.MINING_REWARD
        }), 200
    return jsonify({
        'status': 'fail',
        'reason': 'fail to mining'
    }), 200
    
        
        
        
        
        
        
        
        
        
        
