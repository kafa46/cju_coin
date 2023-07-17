from mining import db
from mining.models import Block
from mining.models import Transaction


class Transfer:
    '''거래 담당 클래스'''
    def __init__(
        self,
        # send_public_key: str,  <- Todo
        send_blockchain_addr: str,
        recv_blockchain_addr: str,
        amount: float,
        # signature: str = None, <- Todo
    ) -> None:
        # self.send_public_key = send_public_key <- Todo
        self.send_blockchain_addr = send_blockchain_addr
        self.recv_blockchain_addr = recv_blockchain_addr
        self.amount = amount
        self.block_id = Block.query.filter(
            Block.timestamp).order_by(Block.timestamp.desc()).first().id
        # self.signature = signature <- Todo
        
    
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
        # Todo
        #   마이닝(채굴)하는 사람은 검증 없이 transaction pool에 추가
        
        # Todo
        #   transaction 검증
        #   is_varified = self.verify_transaction_signature()
        is_verified = True
        if is_verified:
            self.commit_transaction()
            return True
        return False

            
            
            
            
            
        
        
        
        
        
        
        
        
        
    
        
