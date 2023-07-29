from wallet import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    passwd = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_mobile = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    create_date = db.Column(db.DateTime, nullable=True)
    update_date = db.Column(db.DateTime, nullable=True)
    private_key = db.Column(db.String(300), nullable=True)
    public_key = db.Column(db.String(300), nullable=True)
    blockchain_addr = db.Column(db.String(300), nullable=True) # 지갑 주소
    