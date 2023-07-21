from datetime import datetime

from flask import (
    request,
    Blueprint,
    session,
    g, # global variable flask server <-> client
    render_template,
    flash,
    url_for,
    redirect,
)
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from wallet.models import User
from wallet import login_manager
from wallet.forms import SignUpForm, LoginForm
from wallet import db
from wallet.utils.passwd_utils import check_passwd_strength

bp = Blueprint('auth', __name__, url_prefix='/')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.before_app_request
def load_logged_in_user():
    user_key = session.get('user_key')
    if user_key is None:
        g.user = None
    else:
        g.user = User.query.get(user_key)
        
        
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    '''User 로그인'''
    form = LoginForm()
    sign_up_status = request.args.get('sign_up')
    if sign_up_status:
        flash('회원가입에 성공하셨습니다. 축하합니당~')
    
    if request.method=='POST' and form.validate_on_submit():
        data_dic = request.form.to_dict()
        user_id = data_dic.get('user_id')
        passwd = data_dic.get('passwd')
        user = User.query.filter_by(user_id=user_id).first()
        
        if not user:
            flash('존재하지 않는 아이디입니다.')
            return render_template(
                'login.html',
                form=form,
            )
        
        if not check_password_hash(user.passwd, passwd):
            flash('비밀번호가 맞지 않습니다.')
            return render_template(
                'login.html',
                form=form,
            )

        flash(f'로그인 성공! {user.user_id}님 반갑습니다 ^^.')
        
        # 로그인 성공했을 경우
        session.clear
        session['user_id'] = user.user_id # 사용자 아이디
        session['user_key'] = user.id # primary key
        
        login_user(user)
       
        return redirect(
            url_for('main.home', login='success')
        )
    
    return render_template(
        'login.html',
        form=form
    )


@bp.route('/logout/', methods=['GET'])
def logout():
    '''User 로그아웃'''
    session.clear()
    return redirect(url_for('main.home'))


@bp.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    '''회원가입'''
    form = SignUpForm()
    
    if request.method=='POST' and form.validate_on_submit():
        '''회원가입 처리'''
        data_dic = request.form.to_dict()
        print(f'data_dic: {data_dic}')
        user_id = data_dic.get('user_id')
        user = User.query.filter_by(user_id=user_id).first()
        
        if user:
            flash('이미 존재하는 아이디입니다.')
            return render_template('sign_up.html', form=form)
        
        passswd_check_result = check_passwd_strength(data_dic.get('passwd1'))
        if passswd_check_result is not True:
            flash(passswd_check_result)
            return render_template(
                'sign_up.html', form=form
            )
        
        passwd1 = data_dic.get('passwd1')
        passwd2 = data_dic.get('passwd2')
        if passwd1 != passwd2:
            flash('입력하신 비밀번호와 비밀번호 확인이 틀립니다.')
            return render_template(
                'sign_up.html', form=form
            )
        
        # wallet = Wallet() <- To-do
        
        user = User(
            user_id = user_id,
            passwd = generate_password_hash(data_dic.get('passwd1')),
            email = data_dic.get('email'),
            phone_mobile = data_dic.get('phone_mobile'),
            name = data_dic.get('name'),
            create_date = datetime.now(),
            update_date = datetime.now(),
            private_key = 'temp_private_key',
            public_key = 'temp_public_key',
            blockchain_addr = 'temp_blockchain_addr',
        )
        db.session.add(user)
        db.session.commit()
        
        return redirect(
            url_for('auth.login', sign_up='success')
        )
        
    
    return render_template(
        'sign_up.html',
        form=form,
    )
    