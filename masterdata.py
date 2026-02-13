import psycopg2 
import sys 

# 1. Konfigurasi Database PostgreSQL 
db_config = {
    'host': 'localhost',
    'database': 'postgres', 
    'user': 'postgres',
    'password': '', 
    'port': '5432' 
}

def check_database():
    print("================================================")
    print("           SISTEM VALIDASI DATA                 ")
    print("================================================")
    
    try:
        while True:
            print("\n Menunggu Scan Barcode...")
            
            # 2. Input Barcode
            barcode_input = input("Scan Barcode : ").strip()
            
            if not barcode_input:
                continue

            conn = None
            try:
                # 3. Koneksi ke Database
                conn = psycopg2.connect(**db_config)
                cursor = conn.cursor()

                # 4. Query Master Data
                query = "SELECT nama_rawmaterial, susunan_palet, merk_type FROM latihan.master_data WHERE kode_sap = %s"
                cursor.execute(query, (barcode_input,))
                
                result = cursor.fetchone() 

                # 5. Output Hasil
                print("\n" + "="*40)
                if result:
                    nama, palet, merk = result
                    print(f" STATUS   : KODE VALID")
                    print(f" Material : {nama}")
                    print(f" Merk     : {merk}")
                    print(f" Palet    : {palet}") 
                else:
                    print(f" STATUS   : TIDAK VALID")
                    print(f" Kode SAP : {barcode_input}")
                    print(f" Info    : Data tidak ditemukan di database.")
                print("="*40)

            except psycopg2.Error as e:
                print(f"\n DATABASE ERROR: {e}")
            finally:
                if conn:
                    cursor.close()
                    conn.close()
            
    except KeyboardInterrupt:
        print("\n\n[INFO] Menutup aplikasi.")
        sys.exit()

if __name__ == "__main__":
    check_database() 