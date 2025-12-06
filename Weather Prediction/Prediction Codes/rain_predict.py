import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# --- 1. KONEKSI DATABASE ---
DB_CONFIG = {
    'host': '10.60.225.173',
    'user': 'zepun',
    'password': 'ZepunC4&$', 
    'database': 'bmkg_data'
}

def get_data_from_db():
    print("--- [1] Mengambil Data Historis dari MySQL ---")
    conn = mysql.connector.connect(**DB_CONFIG)
    
    # Kita ambil data cuaca yang sudah tersimpan
    query = "SELECT datetime_local, temperature, humidity, wind_speed, weather_desc FROM weather_log"
    
    # Load langsung ke Pandas DataFrame
    df = pd.read_sql(query, conn)
    conn.close()
    
    print(f"Data dimuat: {len(df)} baris.")
    return df

def preprocess_data(df):
    print("--- [2] Membersihkan & Memproses Data ---")
    
    # A. Feature Engineering (Membuat Fitur Baru)
    # Jam sering mempengaruhi hujan (misal: sore sering hujan)
    df['datetime_local'] = pd.to_datetime(df['datetime_local'])
    df['jam'] = df['datetime_local'].dt.hour
    
    # B. Membuat Label Target (Apakah Hujan?)
    # Jika deskripsi mengandung kata 'Hujan' atau 'Rain', kita anggap 1 (True), selain itu 0
    df['is_raining'] = df['weather_desc'].apply(lambda x: 1 if 'hujan' in x.lower() or 'rain' in x.lower() else 0)
    
    # C. Memilih Fitur (X) dan Target (y)
    # Kita gunakan Suhu, Kelembapan, Angin, dan Jam untuk memprediksi Hujan
    features = ['temperature', 'humidity', 'wind_speed', 'jam']
    X = df[features]
    y = df['is_raining']
    
    print("Contoh Data yang akan dipelajari mesin:")
    print(df[['datetime_local', 'temperature', 'humidity', 'weather_desc', 'is_raining']].head())
    
    return X, y

def train_and_predict(X, y):
    print("\n--- [3] Melatih Model Machine Learning (Random Forest) ---")
    
    # A. Bagi data untuk Belajar (Train) dan Ujian (Test)
    # Karena data masih sedikit, kita pakai porsi kecil untuk test
    if len(X) < 10:
        print("[WARNING] Data terlalu sedikit untuk split training/testing yang valid.")
        X_train, X_test, y_train, y_test = X, X, y, y
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # B. Inisialisasi Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # C. Latih Model (Training)
    model.fit(X_train, y_train)
    
    # D. Evaluasi (Cek Kepintaran Model)
    predictions = model.predict(X_test)
    if len(X) >= 10:
        acc = accuracy_score(y_test, predictions)
        print(f"Akurasi Model saat ini: {acc * 100:.2f}%")
    
    return model

def predict_future(model):
    print("\n--- [4] Simulasi Prediksi Masa Depan ---")
    
    # Mari kita coba prediksi cuaca besok dengan skenario buatan
    # Format: [Suhu, Kelembapan, Angin, Jam]
    
    skenario_esok = [
        [32, 60, 10, 12], # Skenario 1: Panas, Kering, Siang jam 12 (Harusnya Tidak Hujan)
        [24, 95, 5, 17],  # Skenario 2: Dingin, Lembap, Sore jam 5 (Harusnya Hujan)
        [27, 85, 20, 20]  # Skenario 3: Malam jam 8
    ]
    
    print("Memprediksi berdasarkan pola data yang sudah dipelajari...")
    column_names = ['temperature', 'humidity', 'wind_speed', 'jam']
    df_future = pd.DataFrame(skenario_esok, columns=column_names)
    
    hasil = model.predict(df_future)
    probabilitas = model.predict_proba(df_future) # Seberapa yakin si mesin?
    
    for i, h in enumerate(hasil):
        kondisi = "AKAN HUJAN 🌧️" if h == 1 else "CERAH / BERAWAN ☀️"
        yakin = probabilitas[i][h] * 100
        
        print(f"\nKasus {i+1}: Suhu {skenario_esok[i][0]}°C, Lembap {skenario_esok[i][1]}%, Jam {skenario_esok[i][3]}.00")
        print(f"-> Prediksi AI: {kondisi} (Keyakinan: {yakin:.1f}%)")

if __name__ == "__main__":
    # 1. Ambil Data
    df_raw = get_data_from_db()
    
    if len(df_raw) > 0:
        # 2. Bersihkan Data
        X, y = preprocess_data(df_raw)
        
        # 3. Latih Otak Buatan
        otak_ai = train_and_predict(X, y)
        
        # 4. Coba Prediksi
        predict_future(otak_ai)
    else:
        print("Database kosong. Jalankan script 'ngehek.py' dulu!")