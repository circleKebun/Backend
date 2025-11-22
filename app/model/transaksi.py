from app import db

class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    
    transaksi_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nama_transaksi = db.Column(db.String(50), nullable = False)
    nominal_transaksi = db.Column(db.Integer, nullable =False)
    tipe_transaksi = db.Column(db.String(50), nullable =False)
    tanggal_transaksi = db.Column(db.DateTime, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.wallet_id'), nullable = False)
    