import requests
import mysql.connector
from app.database import DB_CONFIG

KODE_WILAYAH = "33.25.11.1015"
API_URL = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={KODE_WILAYAH}"

def fetch_and_store():
    print(f"--- [START] Mengambil Data Wilayah: {KODE_WILAYAH} ---")

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data_json = response.json()
    except Exception as e:
        print(f"--- [ERROR API] {e} ---")
        return
    
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        #Data biasanya nested
        try:
            raw_cuaca = data_json["data"][0]["cuaca"]
        except (KeyError, IndexError):
            print("[ERROR JSON] Struktur JSON tidak sesuai.")
            return
        
        cuaca_list = []
        for item in raw_cuaca:
            if isinstance(item, list):
                cuaca_list.extend(item)
            else:
                cuaca_list.append(item)
        
        print(f"[INFO] Total data setelah flatten: {len(cuaca_list)} baris.")

        sql = """
        INSERT IGNORE INTO weather_log
        (adm4_code, datetime_local, temperature, humidity, weather_desc, wind_speed)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        count = 0

        for item in cuaca_list:
            if not isinstance(item, dict):
                continue
            
            tgl = item.get("local_datetime")
            temp = item.get("t", 0)
            hum = item.get("hu", 0)
            desc = item.get("weather_desc", "-")
            ws = item.get("ws", 0.0)

            data = (KODE_WILAYAH, tgl, temp, hum, desc, ws)

            try:
                cursor.execute(sql, data)
                count += cursor.rowcount
            except Exception as e:
                print(f"[ERROR DB] {e}")

        conn.commit()
        print(f"[FINISH] {count} data baru berhasil disimpan.")
        
    except mysql.connector.Error as err:
        print(f"[ERROR DB] {err}")
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if_name_ == "__main__":
    fetch_and_store()