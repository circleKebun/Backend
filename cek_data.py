# Import 'app' biar kita bisa akses database
from server import app 
from app import app,db

# Import model-model yang sudah kamu pisah tadi
from app.model.user import User
from app.model.wallet import Wallet
from app.model.transaksi import Transaksi

# Masuk ke dalam konteks aplikasi Flask
with app.app_context():
    print("=== MULAI CEK KONEKSI ===")

    # 1. Coba ambil semua user
    semua_user = User.query.all()
    print(f"Jumlah User di Database: {len(semua_user)}")
    
    # 2. Kalau ada user, coba print namanya
    if semua_user:
        user_pertama = semua_user[0]
        print(f"User Pertama: {user_pertama.username} (Email: {user_pertama.email})")
        
        # 3. Cek relasi Wallet (Apakah Python bisa nemu dompet user ini?)
        print(f"Dompet milik {user_pertama.username}:")
        for dompet in user_pertama.wallets:
            print(f" - {dompet.nama_wallet} (Saldo: {dompet.saldo})")
            
    else:
        print("Tabel User masih kosong. Coba isi dummy data di DBeaver dulu ya!")

    print("=== SELESAI ===")