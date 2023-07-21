from flask import (
    Blueprint,
    render_template,
)

from wallet.models import User

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def home():
    '''메인 화면'''
    
    return render_template(
        'index.html'
    )
