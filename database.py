import psycopg2

DB_CONFIG = { 
    "host": "localhost",
    "database": "postgres", 
    "user": "postgres",
    "password": "", 
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def simpan_data(teks):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO latihan.barcode (kode_barcode) VALUES (%s)", (teks,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except:
        return False