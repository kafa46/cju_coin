from flask_wtf import FlaskForm
from wtforms import (
    StringField
)
from wtforms.validators import (
    DataRequired,
)


class MinigForm(FlaskForm):
    '''코인 이체 입력 폼'''
    my_blockchain_addr = StringField(
        label='본인의 지갑 주소',
        validators=[
            DataRequired('본인 지갑 주소는 필수입력 사항입니다.'),
        ]
    )