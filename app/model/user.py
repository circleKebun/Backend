from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    
    wallets = db.relationship('Wallet', backref = 'pemilik', lazy =True)
    
    

    
