import collections
import json
import hashlib

from mining.blockchain import BlockChain
from mining.models import Block, Transaction
from mining import config

def sorted_dict_by_key(unsorted_dic: dict):
    # return collections.OrderedDict(
    #     sorted(unsorted_dic.items()), key=lambda keys: keys[0]
    # )
    # return sorted(unsorted_dic.items())
    return dict(sorted(unsorted_dic.items()))
    
def get_blockchain() -> dict:
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


def calculate_total_amount(blockchain_addr: str) -> float:
    '''blockchain_addr에 해당하는 계좌 총액(float) 구하기'''
    total_amount = 0.0
    chain = get_blockchain()
    for block in chain['chain']:
        # 체인으로 연결된 모든 블록 조사
        for transaction in block['transactions']:
            value = float(transaction['amount'])
            if blockchain_addr == transaction['recv_blockchain_addr']:
                total_amount += value
            if blockchain_addr == transaction['send_blockchain_addr']:
                total_amount -= value
    
    return total_amount

def get_prev_hash() -> str:
    '''DB에서 마지막 블록의 prev_hash 찾아서 리턴'''
    prev_hash = Block.query.filter(
        Block.timestamp,
    ).order_by(Block.timestamp.desc()).first().prev_hash
    return prev_hash


def valid_proof(
    challenge: int,
    prev_hash: str,
    transactions: list
) -> bool:
    ''''Difficult 개수만큼 0 일치하는지 검사하여 True/False 리턴'''
    # challange + prev_hash + transaction_pool
    guess_block = sorted_dict_by_key(
        {
            'transactions': transactions,
            'nonce': challenge,
            'prev_hash': prev_hash
        }
    )
    guess_block_hash = hash(guess_block)
    result = guess_block_hash[:config.MINING_DIFFICULTY] == '0'*config.MINING_DIFFICULTY
    # print(f'result: {result}')
    return result
