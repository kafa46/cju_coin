import os
import requests

from p2p.secret import csrf_token_secret

BASE_DIR = os.path.dirname(__file__)

# SQLAlchemy 사용할 DB 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
    os.path.join(BASE_DIR, 'p2p.db')
)

# CSRF TOKEN secret key
SECRET_KEY = csrf_token_secret

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