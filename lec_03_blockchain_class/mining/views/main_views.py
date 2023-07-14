from flask import (
    Blueprint,
    jsonify,
)
from mining.utils.blockchain_utils import get_blockchain

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def home():
    '''Mining 메인화면'''
    return 'hello world'

@bp.route('/get_chain/', methods=['GET'])
def get_chain():
    block_chain = get_blockchain()
    response = {
        'chain': block_chain.get('chain')
    }
    return jsonify(response), 200
