export FLASK_APP=wallet
export FLASK_DEBUG=True

echo
echo '가상환경을 활성화 합니다.'
. venv/bin/activate

flask run -h 0.0.0.0 -p 8080