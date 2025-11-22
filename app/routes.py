from app import app,db
from flask import jsonify, request
from datetime import datetime

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
    
#transaksi baru

@app.route("/transaksi", methods = ['POST'])
def transaksi_baru():
    data = request.get_json()  #ambil data dari user input
    
    u_id = data['user_id']
    w_id = data['wallet_id']
    nominal = int(data['nominal'])
    tipe = data['tipe']
    
    dompet = Wallet.query.filter_by(wallet_id = w_id, user_id = u_id).first()
    
    if not dompet:
        return jsonify({"pesan": "Dompet tidak ditemukan"}),404
    
    saldo_awal = dompet.saldo

    if tipe == 'Pengeluaran' and dompet.saldo < nominal:
        return jsonify({"pesan": "Saldo tidak cukup!"}),400
    
    if tipe == 'Pengeluaran':
        dompet.saldo = dompet.saldo - nominal
    
    if tipe == 'Pemasukan':
        dompet.saldo = dompet.saldo + nominal
        
    transaksi_baru = Transaksi(
        nama_transaksi = data['nama_transaksi'],
        nominal_transaksi = nominal,
        tipe_transaksi = tipe,
        tanggal_transaksi = datetime.now(),
        user_id = u_id,
        wallet_id = w_id
    )
    
    try:
        db.session.add(transaksi_baru)

        db.session.commit()

        return jsonify({
            "pesan" : "Transaksi Berhasil",
            "dompet" : dompet.nama_wallet,
            "saldo_awal" : saldo_awal,
            "saldo_akhir" : dompet.saldo
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"pesan": "Gagal mencatat transaksi", "error": str(e)}), 400
    
#history transaksi

@app.route('/transaksi', methods=['GET'])
def history_transaksi():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"pesan" : "User ID Wajib diisi"})

    list_transaksi = Transaksi.query.filter_by(user_id = user_id).all()

    hasil =[]
    for i in list_transaksi:
        hasil.append({
            "id": i.transaksi_id,
            "nama" : i.nama_transaksi,
            "nominal" : i.nominal_transaksi,
            "tipe" : i.tipe_transaksi,
            "tanggal" : i.tanggal_transaksi,
            "wallet_id" : i.wallet_id
        })
    return jsonify(hasil)

#hapus transaksi
@app.route('/transaksi/<int:transaksi_id>', methods=['DELETE'])
def hapus_transaksi(transaksi_id):
    
    t = Transaksi.query.get(transaksi_id)

    if not t:
        return jsonify({"pesan": "Transaksi tidak ditemukan"}), 404
    
    dompet = Wallet.query.get(t.wallet_id)

    if t.tipe_transaksi == 'Pengeluaran':
        dompet.saldo = dompet.saldo + t.nominal_transaksi
    elif t.tipe_transaksi == 'Pemasukan':
        dompet.saldo = dompet.saldo - t.nominal_transaksi
    
    try:
        db.session.delete(t)
        db.session.commit()

        return jsonify({
            "pesan" : "Transaksi berhasil dihapus",
            "saldo_dikembalikan" : dompet.saldo
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"pesan": "Gagal hapus transaksi", "error":str(e)}),400
    