from mining import db

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prev_hash = db.Column(db.String(300), nullable=True)
    nonce = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.Float)

    
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey('block.id', ondelete="CASCADE"))
    send_addr = db.Column(db.String(300))
    recv_addr = db.Column(db.String(300))
    amount = db.Column(db.Float)
    blockchain = db.relationship(
        'Block',
        backref=db.backref('transactions')
    )
    
    