import pandas as pd
import mysql.connector
import os

# Lokasi folder dataset
OUTPUT_DIR = "ml_model/dataset"
OUTPUT_PATH = f"{OUTPUT_DIR}/weather_data.csv"

# Konfigurasi database (samakan dengan app/database.py)
DB_CONFIG = {
    "host": "localhost",
    "user": "zepun",
    "password": "ZepunC4&$",
    "database": "bmkg_data",
}


def export_dataset():
    print("[EXPORT] Mengambil data dari MySQL...")

    # Koneksi DB
    conn = mysql.connector.connect(**DB_CONFIG)
    query = """
        SELECT 
            adm4_code,
            datetime_local,
            temperature,
            humidity,
            wind_speed,
            weather_desc
        FROM weather_log
        ORDER BY datetime_local ASC
    """

    df = pd.read_sql(query, conn)
    conn.close()

    print(f"[EXPORT] Total {len(df)} baris data berhasil diambil.")

    # Pastikan folder ml_model/dataset ada
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Simpan ke CSV
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print(f"[SUCCESS] Dataset disimpan ke: {OUTPUT_PATH}")


if __name__ == "__main__":
    export_dataset()