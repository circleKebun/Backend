Backend API Documentation

Base URL: http://localhost:5000 (atau IP LAN)

1. POST /users (Register) -> Body: {username, email, password}
2. POST /login (Login) -> Body: {email, password}
3. POST /wallets (Bikin Dompet) -> Body: {user_id, nama_wallet, saldo}
4. GET /wallets?user_id=1 (Lihat Dompet)
5. POST /transaksi (Catat) -> Body: {user_id, wallet_id, nama_transaksi, nominal, tipe}
   *tipe: 'Pemasukan' atau 'Pengeluaran'
6. GET /transaksi?user_id=1 (Riwayat)
7. DELETE /transaksi/<id> (Hapus & Balikin Saldo)