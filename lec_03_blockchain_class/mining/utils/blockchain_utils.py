import collections
import json
import hashlib

from mining.blockchain import BlockChain
from mining.models import Block, Transaction

def sorted_dict_by_key(unsorted_dic: dict):
    return collections.OrderedDict(
        sorted(unsorted_dic.items()), key=lambda keys: keys[0]
    )
    
    
def get_blockchain():
    '''데이터베이스로부터 블록체인 정보 가져오기'''
    blockchain_exist = Block.query.all()
    if not blockchain_exist:
        blockchain = BlockChain()
        blockchain.create_genesis_block()
    
    return build_blockchain_json()


def build_blockchain_json() -> dict:
    '''DB로부터 모든데이터 추출하여 dict 가공해서 리턴'''
    # DB에 있는 모든 정보 불러오기
    blocks = Block.query.filter(
        Block.timestamp
    ).order_by(Block.timestamp)
   
    
    # 리턴할 dict 정의
    result_dic = {
        'chain': [],
        'transaction_pool': [],
    }
    for block in blocks:
        result_dic['chain'].append(
            {
                'nonce': block.nonce,
                'prev_hash': block.prev_hash,
                'timestamp': block.timestamp,
                'transactions': get_transaction_list(block)
            }
        )
    
    # 가장 최근(마지막) 생성된 블록일 경우 -> transaction_pool 생성
    last_block = Block.query.filter(
        Block.timestamp,
    ).order_by(Block.timestamp.desc()).first()
    result_dic['transaction_pool'] = get_transaction_list(last_block)
    print('hello')
    return result_dic

def get_transaction_list(block: Block) -> list:
    '''Block에 해당하는 transaction 객체를 리턴'''
    transaction_exist = Transaction.query.all()
    if not transaction_exist:
        return []
    
    transaction_list = []
    transactions = block.transactions
    for transaction in transactions:
        transaction_list.append(
            {
                'send_blockchain_addr': transaction.send_addr,
                'recv_blockchain_addr': transaction.recv_addr,
                'amount': transaction.amount,
            }
        )
    return transaction_list


def hash(block: dict) -> str:
    sorted_block = json.dumps(block, sort_keys=True)
    return hashlib.sha256(sorted_block.encode()).hexdigest()