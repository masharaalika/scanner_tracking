import psycopg2

# 1. Konfigurasi Database PostgreSQL (Sesuaikan password DBeaver kamu)
db_config = {
    'host': 'localhost',
    'database': 'postgres', # Nama database utama
    'user': 'postgres',
    'password': '', 
    'port': '5432'
}

def check_database():
    print("=== PROGRAM PENGECEKAN BARCODE ===")
    
    while True:
        # Input dari scanner
        barcode_input = input("\nScan Barcode: ")
        
        if not barcode_input:
            continue

        try:
            # 2. Koneksi ke PostgreSQL
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # 3. Query mencari di tabel master_data (dalam schema latihan)
            # cari berdasarkan kolom 'kode_sap'
            query = "SELECT nama_rawmaterial, susunan_palet, merk_type FROM latihan.master_data WHERE kode_sap = %s"
            cursor.execute(query, (barcode_input,))
            
            result = cursor.fetchone()

            # 4. Logika Validasi
            if result:
                nama, palet, merk = result
                print("------------------------------------------")
                print(f" KODE VALID!")
                print(f" Nama Material : {nama}")
                print(f" Merk Type     : {merk}")
                print(f" Susunan Palet : {palet}")
                print("------------------------------------------")
            else:
                print("------------------------------------------")
                print(f" KODE TIDAK VALID: [{barcode_input}]")
                print("Keterangan: Data tidak ditemukan di database.")
                print("------------------------------------------")

            
            cursor.close()
            conn.close()

        except Exception as e:
            print(f" Gagal terhubung ke database: {e}")
            break

if __name__ == "__main__":
    check_database()