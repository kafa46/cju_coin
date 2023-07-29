'''지갑 wallet 거래 담당 기능 구현'''

import hashlib
import codecs
import base58
from pprint import pprint

from ecdsa import NIST256p, SigningKey

from wallet.utils import dict_utils


class Wallet:
    '''씨쥬 코인 전자지갑'''
    def __init__(self) -> None:
        '''객체 생성할 때 초기화'''
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()
    
    @property
    def blockchain_address(self) -> str:
        '''생성된 지갑 주소 리턴'''
        return self._blockchain_address
        
    @property
    def private_key(self) -> str:
        '''Private Key를 문자열로 변환하여 리턴'''
        return self._private_key.to_string().hex()
        
    @property
    def public_key(self) -> str:
        '''Public Key를 문자열로 변환하여 리턴'''
        return self._public_key.to_string().hex()
        
    
    def generate_blockchain_address(self) -> str:
        '''블록체인(지갑) 주소 생성'''
        # Step 1. private/public key 생성 -> __init__ 에서 이미 생성(생략)
        # Step 2. Public key에 SHA-256 수행
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        # Step 3. SHA-256 수행 결과에 RipeMD160 수행
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_digest_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        # Step 4. Network byte 추가
        network_coin_public_key = b'00' + ripemd160_bpk_digest_hex
        network_coin_public_key_bytes = codecs.decode(
            network_coin_public_key, 
            'hex'
        )
        # Step 5. SHA-256 2회 수행
        sha256_bpk_digest = hashlib.sha256(network_coin_public_key_bytes).digest()
        sha256_2_bpk_digest = hashlib.sha256(sha256_bpk_digest).digest()
        sha256_hex = codecs.encode(sha256_2_bpk_digest, 'hex')
        # Step 6. Checksum 구하기
        checksum = sha256_hex[:8]
        
        # Step 7. Public Key에 Checksum 더하기
        # addr_hex = (sha256_hex + checksum).decode('utf-8')
        addr_hex = (network_coin_public_key + checksum).decode('utf-8')
        
        # Step 8. 더한 키를 Base58로 인코딩
        blockchain_addr = base58.b58encode(addr_hex).decode('utf-8')
        
        return blockchain_addr
    
    @staticmethod
    def generate_signature(
        send_blockchain_addr: str,
        recv_blockchain_addr: str,
        send_private_key: str,
        amount: float
    ) -> str:
        '''거래에 필요한 signature 생성'''
        transaction = dict_utils.sorted_dict_by_key(
            {
                'send_blockchain_addr': send_blockchain_addr,
                'recv_blockchain_addr': recv_blockchain_addr,
                'amount': float(amount),
            }
        )
        sha256 = hashlib.sha256()
        print('transaction')
        pprint(transaction)        
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        print(f'message: {message}')
        private_key = SigningKey.from_string(
            bytes().fromhex(send_private_key),
            curve=NIST256p
        )
        # 거래내역(transaction message)를 Private Key로 서명 
        private_key_sign = private_key.sign(message)
        signature = private_key_sign.hex()
        
        return signature
        
    
    # def calculate_total_amount(self,) -> float:
    #     '''blockchain_addr에 해당하는 계좌 총액을 구해서 리턴
    #         --> Blockchain node에 요청하여 값을 얻어오는 것으로 구현
    #             Wallet 서버에서 Javascript로 별도 구현
    #     '''
    