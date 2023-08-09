import time
from typing import Union

from p2p.models import MiningNode
from p2p import db


def add_new_node(ip: str, port: str) -> None:
    '''새로운 노드 정보를 DB에 추가'''
    node = MiningNode()
    node.ip = ip
    node.port = port
    node.timestamp = time.time()
    db.session.add(node)
    db.session.commit()


def check_node_exist(ip: str, port: str) -> Union[bool, MiningNode]:
    '''IP, Port 일치하는 노드가 있는지 확인
        없다면 False 리턴, 있다면 해당 객체 리턴'''
    node = MiningNode.query.filter(
        MiningNode.ip==ip, 
        MiningNode.port==port
    ).first()
    print(f'node: {node}')
    if not node:
        return False
    return node