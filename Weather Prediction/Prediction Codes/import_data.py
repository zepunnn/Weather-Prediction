import requests
import mysql.connector

# --- 1. KONFIGURASI DATABASE ---
DB_CONFIG = {
    'host': '10.60.225.173',
    'user': 'zepun',
    'password': 'ZepunC4&$', 
    'database': 'bmkg_data'
}

KODE_WILAYAH = "33.25.11.1015"
API_URL = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={KODE_WILAYAH}"

def fetch_and_store():
    print(f"--- [START] Mengambil Data Wilayah: {KODE_WILAYAH} ---")
    
    # --- 2. AMBIL DATA DARI API ---
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data_json = response.json()
    except Exception as e:
        print(f"[ERROR API] {e}")
        return

    # --- 3. KONEKSI DATABASE ---
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Ambil data mentah
        try:
            raw_cuaca = data_json['data'][0]['cuaca']
        except (KeyError, IndexError):
            print("[ERROR JSON] Struktur data tidak sesuai.")
            return

        # --- LOGIKA FLATTEN (MEMBUKA LIST DI DALAM LIST) ---
        # Ini langkah penting untuk memperbaiki error 'list object has no attribute get'
        cuaca_list_bersih = []
        for item in raw_cuaca:
            if isinstance(item, list):
                # Jika item adalah list, kita ambil isinya (extend)
                cuaca_list_bersih.extend(item)
            else:
                # Jika item sudah dictionary, langsung masukkan
                cuaca_list_bersih.append(item)

        print(f"[INFO] Total data ditemukan setelah dirapikan: {len(cuaca_list_bersih)} baris.")

        # --- 4. PROSES PENYIMPANAN ---
        sql = """
            INSERT IGNORE INTO weather_log 
            (adm4_code, datetime_local, temperature, humidity, weather_desc, wind_speed) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        success_count = 0
        
        for item in cuaca_list_bersih:
            # Pastikan item benar-benar Dictionary sebelum diproses
            if not isinstance(item, dict):
                continue 

            # Mengambil nilai menggunakan .get() agar aman
            tgl   = item.get('local_datetime')
            temp  = item.get('t', 0)
            hum   = item.get('hu', 0)
            desc  = item.get('weather_desc', '-')
            ws    = item.get('ws', 0.0)

            val = (KODE_WILAYAH, tgl, temp, hum, desc, ws)

            try:
                cursor.execute(sql, val)
                success_count += cursor.rowcount
            except mysql.connector.Error as e:
                print(f"[ERROR SQL] Gagal insert: {e}")

        conn.commit()
        print(f"[FINISH] Berhasil menyimpan {success_count} data baru.")
        print("-------------------------------------------------------")

    except mysql.connector.Error as err:
        print(f"[ERROR KONEKSI DB] {err}")
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    fetch_and_store()