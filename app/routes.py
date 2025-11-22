from app import app,db
from flask import jsonify, request
from app.model.user import User
from app.model.wallet import Wallet
from app.model.transaksi import Transaksi

@app.route('/users', methods=['GET'])
def get_all_user():
    semua_user = User.query.all()

    hasil = []

    for u in semua_user:
        data = {
            "id" : u.user_id,
            "username" : u.username,
            "email" : u.email
        }
        hasil.append(data)
    return jsonify(hasil)

# bikin user baru
@app.route('/users', methods = ['POST'])
def create_user():
    data = request.get_json()

    user_baru = User(
        username = data['username'],
        email = data['email'],
        password = data['password']
    )
    
    try:
        db.session.add(user_baru)
        db.session.commit()

        return jsonify({"pesan" : "Berhasil bikin user!", "id": user_baru.user_id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"pesan" : "Gagal bikin user", "error" : str(e)}), 400
    
    
# bikin wallet baru
    
@app.route('/wallets', methods = ['POST'])
def new_wallet():
    data = request.get_json()
    
    wallet_baru = Wallet(
        user_id = data['user_id'],
        nama_wallet = data['nama_wallet'],
        saldo = data['saldo']
    )
    
    try:
        db.session.add(wallet_baru)
        db.session.commit()
        return jsonify({
            "pesan" : "berhasil menambahkan wallet!",
            "id" : wallet_baru.wallet_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "pesan" : "Gagal menambahkan wallet",
            "error" : str(e)
        }), 400
    
#liat saldo wallet

@app.route('/wallets', methods = ['GET'])
def get_wallet():
    
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"pesan" : "tolong kasih user_id di URL! Contoh: /wallets?user_id=1"}), 400
    
    dompet_user = Wallet.query.filter_by(user_id = user_id).all()

    hasil = []
    for w in dompet_user:
        hasil.append({
            "id" : w.wallet_id,
            "nama" : w.nama_wallet,
            "saldo" : w.saldo
        })
    return jsonify(hasil)
    