import contextlib
import threading

from typing import List, Tuple

from mining.transfer import Transfer
from mining.config import (
    MINING_DIFFICULTY,
    BLOCKCHAIN_NETWORK, 
    MINING_REWARD,
)
from mining.utils import blockchain_utils
from mining.blockchain import BlockChain
from mining import config
from mining import create_app

class Mine:
    '''블록체인 채굴(mining) 클래스'''
    
    def __init__(
        self,
        difficulty: int = MINING_DIFFICULTY,
        reward: float = MINING_REWARD,
    ) -> None:
        '''채굴 객체 초기화'''
        self.difficulty = difficulty
        self.reward = reward
        self.mining_semaphore = threading.Semaphore(1)
        self.sync_neighbours_semaphore = threading.Semaphore(1)
        
    
    def proof_of_work(self, transaction_pool: List[dict]) -> int:
        '''Nonce 값을 찾아서 리턴'''   
        # challange + prev_hash + transaction_pool
        prev_hash = blockchain_utils.get_prev_hash()
        challenge = 0
        while blockchain_utils.valid_proof(challenge, prev_hash, transaction_pool) is False:
            challenge += 1
        return challenge # 이때 challenge 값 -> nonce
    
    
    def mining(self, recv_blockchain_addr) -> Tuple[bool, str]:
        '''채굴 수행 -> 성공 여부(True|False) 리턴'''
        app = create_app()
        with app.app_context():
            print('start mining from Mine.mining')
            # 채굴자 보상 -> transfer 객체 이용
            transfer = Transfer(
                send_public_key='',
                send_blockchain_addr=BLOCKCHAIN_NETWORK,
                recv_blockchain_addr=recv_blockchain_addr,
                amount=self.reward,
            )
            transfer.add_transaction()
            
            # Proof of work 수행
            block_chain = blockchain_utils.get_blockchain()
            prev_block = block_chain.get('chain')[-1]
            transaction_pool_after_add_transaction = block_chain.get('transaction_pool')
            nonce = self.proof_of_work(transaction_pool_after_add_transaction)
            print(f'Nonce found: {nonce}')
            
            # 새로운 블록 생성
            prev_block_sorted = blockchain_utils.sorted_dict_by_key(prev_block)
            prev_hash = blockchain_utils.hash(prev_block_sorted)
            block_chain_obj = BlockChain()
            block_chain_obj.create_block(
                nonce=nonce,
                prev_hash=prev_hash,
            )
            print('채굴 성공')
            return (True, 'success')
    
    def start_mining(self, recv_blockcain_addr: str) -> None:
        '''세마포를 이용하여 지속적으로 마이닝 반복'''
        def mining_thread():
            while True:
                self.mining(recv_blockcain_addr)
                if config.STOP_MINING:
                    print('코인 채굴을 중단합니다 in Mining.start_mining')
                    config.STOP_MINING = False
                    break
        trd = threading.Thread(target=mining_thread)
        trd.daemon = True # 메인 프로그램이 중지되면 채굴도 중단
        trd.start()
