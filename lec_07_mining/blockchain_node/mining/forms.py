from flask_wtf import FlaskForm
from wtforms import (
    StringField,
)
from wtforms.validators import (
    DataRequired,
)


class MiningForm(FlaskForm):
    '''채굴자 지갑주소(blockchain_addr) 입력 폼'''
    my_blockchain_addr = StringField(
        label='채굴자 지갑 주소',
        validators=[
            DataRequired('채굴 보상금을 지급하기 위한 지갑주소(blockchain address)를 반드시 입력해야 합니다.')
        ]
    )