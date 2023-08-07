import base64
import os
import requests

from mining.secret import csrf_token_secret

BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABSE
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
    os.path.join(BASE_DIR, 'blockchain.db')
)

# ORM 변경사항 -> 추적 X
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 비밀키
SECRET_KEY = csrf_token_secret


# 채굴 성공 -> 채굴 보상금
BLOCKCHAIN_NETWORK = 'BLOCK CHAIN NETWORK'

# Mining difficult
MINING_DIFFICULTY = 5

# Mining Reward
MINING_REWARD = 15.0

# 채굴 중단 flag
STOP_MINING = True
