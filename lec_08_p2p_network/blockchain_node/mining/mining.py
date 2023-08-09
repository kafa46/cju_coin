import threading
import requests

from typing import List, Tuple
from mining.utils import blockchain_utils
from mining.transfer import Transfer
from .config import (
    BLOCKCHAIN_NETWORK,
    MINING_DIFFICULTY,
    MINING_REWARD,
    MY_PUBLIC_IP,
)
from mining.blockchain import BlockChain
from mining import config
from mining import create_app


class Mine:
    '''블록체인 채굴(mining) 클래스'''
    def __init__(
        self,
        difficulty: int = MINING_DIFFICULTY, # 채굴 난이도
        reward: float = MINING_REWARD, # 채굴 보상금
    ) -> None:
        self.difficulty = difficulty
        self.reward = reward


    def proof_of_work(self, transaction_pool: List[dict]) -> int:
        prev_hash = blockchain_utils.get_prev_hash() # 마지막 블록 추출
        nonce: int = 0 # 마이닝 시작: 챌린지 0부터
        while blockchain_utils.valid_proof(transaction_pool, prev_hash, nonce) is False:
            nonce += 1
        return nonce


    def mining(self, recv_blockcain_addr) -> Tuple[bool, str]:
        '''마이닝 수행 -> 성공 여부(True/False) 리턴'''
        app = create_app()
        with app.app_context():
            transfer = Transfer(
                send_public_key='',
                send_blockchain_addr=BLOCKCHAIN_NETWORK,
                recv_blockchain_addr=recv_blockcain_addr,
                amount=self.reward
            )
            transfer.add_transaction()

            prev_block = blockchain_utils.get_blockchain().get('chain')[-1]
            transaction_pool_after_add_transaction = prev_block['transactions']
            nonce = self.proof_of_work(transaction_pool_after_add_transaction)
            prev_block_sorted = blockchain_utils.sorted_dict_by_key(prev_block)
            prev_hash = blockchain_utils.hash(prev_block_sorted)
            
            block_chain_obj = BlockChain()
            block_chain_obj.create_block(
                nonce=nonce,
                prev_hash=prev_hash
            )
            print('채굴 성공!')
            
            # 채굴에 성공하면 P2P 이웃 노드에게 정보 업데이트 요청
            url = f'http://{config.MY_PUBLIC_IP}:{config.PORT_P2P}/neighbors'
            resp = requests.get(url)
            neighbors_dic = resp.json()
            for neighbor in neighbors_dic.values():
                json_data = {
                    'ip': config.MY_PUBLIC_IP,
                    'port': config.PORT_P2P
                }
                try:
                    url_update = f"http://{neighbor['ip']}:{config.PORT_P2P}/update/"
                    resp = requests.get(url_update, params=json_data, timeout=2)
                    if resp.status_code != 200:
                        print(f'Sync neighbor fail on {url_update}')
                except:
                    print(f'Sync process failed')
            
            # 이웃 노드에게 consensus algorithm (resolve_conflicts)
            # 실행하도록 요청
            url_resolve_conflict = f"http://{config.MY_PUBLIC_IP}:{config.PORT_P2P}/neighbors"
            resp = requests.get(url_resolve_conflict)
            neighbors_dic = resp.json()
            for neighbor in neighbors_dic.values():
                ip, port = neighbor['ip'], neighbor['port']
                if ip==config.MY_PUBLIC_IP and port==config.PORT_P2P:
                    continue
                neighbor_url = f'http://{ip}:{config.PORT_MINING}/resolve_conflict'
                try:
                    resp_resolve = requests.get(neighbor_url)
                    if resp_resolve.status_code == 200:
                        print('Success resolve conflict')
                except:
                    print(f'Cannot connect to {neighbor_url}')
                    return (False, 'fail')
            
            return (True, 'success')


    def start_mining(self, recv_blockcain_addr: str) -> None:
        '''연속적으로 채굴(마이닝) 수행'''
        def mining_thread():
            while True:
                self.mining(recv_blockcain_addr)
                if config.STOP_MINING:
                    print('코인 채굴을 중단합니다. in Mining.start_mining')
                    config.STOP_MINING = False
                    break
        trd = threading.Thread(target=mining_thread)
        trd.daemon = True #  메인 프로그램이 중지되면 백그라운드 채굴도 중단
        trd.start()
        
        