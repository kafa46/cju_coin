import time

from mining import db
from mining.models import Block
from mining.utils import blockchain_utils

class BlockChain:
    '''블록체인 클래스'''
    def __init__(self) -> None:
        pass
    
    def create_genesis_block(self,) -> bool:
        '''Genesis Block 생성'''
        block_exist = Block.query.all()
        if block_exist:
            print({
                'status': 'Fail to create genesis block',
                'error': 'Block(s) aleady exist'
            })
            return False
        
        genesis_block = Block(
            prev_hash = blockchain_utils.hash({}),
            nonce = 0,
            timestamp = time.time()
        )
        db.session.add(genesis_block)
        db.session.commit()
        
        return True
    
    
    def create_block(self, nonce: int, prev_hash: str = None):
        '''블록체인에서 새로운 블록 생성'''
        try:
            db.session.add(
                Block(
                    prev_hash = prev_hash,
                    nonce = nonce,
                    timestamp = time.time()                
                )
            )
            db.session.commit()
        except Exception as e:
            print('Fail to block on database')
            print(f'Error: {e}')
            return False