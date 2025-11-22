from app import db


class Wallet(db.Model):
    __tablename__ = 'wallet'

    wallet_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nama_wallet = db.Column(db.String(50), nullable = False)
    saldo = db.Column(db.BigInteger, default = 0)
    
    user_id = db.Column(db.Integer, db.ForeignKey ('user.user_id'), nullable = False)

    transaksi = db.relationship('Transaksi', backref = 'sumber_dana', lazy=True)