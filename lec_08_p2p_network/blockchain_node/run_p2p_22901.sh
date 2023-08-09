echo 

echo '가상환경을 활성화 합니다.'
. venv/bin/activate

echo
echo 'Start P2P Server'
export FLASK_APP=p2p
export FLASK_DEBUG=True
flask run -h 0.0.0.0 -p 22901