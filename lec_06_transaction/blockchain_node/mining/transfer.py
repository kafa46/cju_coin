import hashlib

from ecdsa import NIST256p, VerifyingKey

from mining import db
from mining.models import Block
from mining.models import Transaction
from mining.utils import blockchain_utils


class Transfer:
    '''거래 담당 클래스'''
    def __init__(
        self,
        send_public_key: str, 
        send_blockchain_addr: str,
        recv_blockchain_addr: str,
        amount: float,
        signature: str = None
    ) -> None:
        self.send_public_key = send_public_key
        self.send_blockchain_addr = send_blockchain_addr
        self.recv_blockchain_addr = recv_blockchain_addr
        self.amount = amount
        self.block_id = Block.query.filter(
            Block.timestamp).order_by(Block.timestamp.desc()).first().id
        self.signature = signature
        
    
    def commit_transaction(self) -> None:
        '''Commit transaction into DB'''
        transaction = Transaction(
            block_id = self.block_id,
            send_addr = self.send_blockchain_addr,
            recv_addr = self.recv_blockchain_addr,
            amount = float(self.amount)
        )
        db.session.add(transaction)
        db.session.commit()
        
    
    def add_transaction(self) -> bool:
        '''Add a transaction into DB'''
        
        transaction = blockchain_utils.sorted_dict_by_key(
            {
                'send_blockchain_addr': self.send_blockchain_addr,
                'recv_blockchain_addr': self.recv_blockchain_addr,
                'amount': float(self.amount)
            }
        )
        
        # Todo
        #   마이닝(채굴)하는 사람은 검증 없이 transaction pool에 추가
        
        is_verified = self.verify_transaction_signature(
            self.send_public_key,
            self.signature,
            transaction
        )
        if is_verified:
            self.commit_transaction()
            return True
        return False

    
    def verify_transaction_signature(
        self,
        send_public_key: str,
        signature: str,
        transaction: dict
    ) -> bool:
        '''거래(transaction) 서명(signature) 검증 후 True/False 리턴'''
        # 검증 과정 수행
        sha256 = hashlib.sha256()
        sha256.update(str(transaction).encode('utf-8'))
        mssage = sha256.digest()
        signature_byte = bytes().fromhex(signature)
        verifying_key = VerifyingKey.from_string(
            bytes().fromhex(send_public_key),
            curve=NIST256p
        )
        is_verified = verifying_key.verify(
            signature=signature_byte,
            data=transaction
        )
        return is_verified # True if the verification was successful
            
            
            
            
        
        
        
        
        
        
        
        
        
    
        
