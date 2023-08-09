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

# 자신의 공인 아이피를 확인하기 위해 이용하는 서비스 프로바이더
# Other possible service providers
#   - https://ident.me
#   - https://api.ipify.org
#   - https://myip.dnsomatic.com
IP_CHECK_SERVICE_PROVIDER = 'https://checkip.amazonaws.com'

# My Host Information
MY_PUBLIC_IP = requests.get(IP_CHECK_SERVICE_PROVIDER).text.strip()

# Seed Node IP addr
SEED_NODE_IP = '203.252.240.43'

# P2P Network Port Number
PORT_P2P = '22901'

# Mining node Port #
PORT_MINING = '7001'