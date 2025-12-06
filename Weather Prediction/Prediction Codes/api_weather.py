import mysql.connector
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import uvicorn

# --- 1. KONFIGURASI DATABASE ---
DB_CONFIG = {
    'host': '10.60.225.173',
    'user': 'zepun',
    'password': 'ZepunC4&$', 
    'database': 'bmkg_data'
}

# --- 2. INISIALISASI FASTAPI ---
app = FastAPI(
    title="API Prediksi Hujan",
    description="Backend Machine Learning untuk memprediksi cuaca berdasarkan data historis BMKG.",
    version="1.0"
)

# Variabel Global untuk menyimpan Otak Buatan (Model)
GLOBAL_MODEL = None
MODEL_ACCURACY = 0.0

# --- 3. DEFINISI STRUKTUR DATA (PYDANTIC) ---
# Ini mencegah error tipe data (Validasi Otomatis)
class WeatherInput(BaseModel):
    temperature: float  # Contoh: 28.5
    humidity: int       # Contoh: 80
    wind_speed: float   # Contoh: 10.5
    jam: int            # Contoh: 14 (Jam 2 Siang)

class PredictionResponse(BaseModel):
    status: str
    prediksi: str
    probabilitas_hujan: float
    pesan: str

# --- 4. FUNGSI TRAINING MODEL (Dijalankan saat Start-up) ---
def train_model():
    print("[INIT] Sedang melatih model dari database...")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        query = "SELECT datetime_local, temperature, humidity, wind_speed, weather_desc FROM weather_log"
        df = pd.read_sql(query, conn)
        conn.close()

        if len(df) < 10:
            print("[WARNING] Data terlalu sedikit. Model mungkin tidak akurat.")
            return None, 0.0

        # Feature Engineering
        df['datetime_local'] = pd.to_datetime(df['datetime_local'])
        df['jam'] = df['datetime_local'].dt.hour
        
        # Labeling (1 = Hujan, 0 = Tidak)
        df['is_raining'] = df['weather_desc'].apply(lambda x: 1 if 'hujan' in x.lower() or 'rain' in x.lower() else 0)

        # Features & Target
        X = df[['temperature', 'humidity', 'wind_speed', 'jam']]
        y = df['is_raining']

        # Training
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Cek Akurasi
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        
        print(f"[SUCCESS] Model siap! Akurasi: {acc * 100:.2f}%")
        return model, acc

    except Exception as e:
        print(f"[ERROR TRAINING] {e}")
        return None, 0.0

# --- 5. EVENT: SAAT SERVER NYALA ---
@app.on_event("startup")
def startup_event():
    global GLOBAL_MODEL, MODEL_ACCURACY
    GLOBAL_MODEL, MODEL_ACCURACY = train_model()

# --- 6. ENDPOINT API ---

@app.get("/")
def home():
    return {
        "message": "API Prediksi Cuaca Online",
        "model_status": "Ready" if GLOBAL_MODEL else "Not Ready (Not enough data)",
        "current_accuracy": f"{MODEL_ACCURACY * 100:.2f}%"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_weather(data: WeatherInput):
    # Cek apakah model sudah ada
    if GLOBAL_MODEL is None:
        raise HTTPException(status_code=503, detail="Model belum siap atau data database kosong.")

    # Konversi data input ke format DataFrame
    # Urutan kolom HARUS SAMA dengan saat training
    input_data = pd.DataFrame([{
        'temperature': data.temperature,
        'humidity': data.humidity,
        'wind_speed': data.wind_speed,
        'jam': data.jam
    }])

    # Lakukan Prediksi
    hasil = GLOBAL_MODEL.predict(input_data)[0]
    probabilitas = GLOBAL_MODEL.predict_proba(input_data)[0][1] # Ambil probabilitas kelas "1" (Hujan)

    # Susun Kalimat Jawaban
    if hasil == 1:
        teks_prediksi = "HUJAN 🌧️"
        pesan_saran = "Sediakan payung jika ingin keluar."
    else:
        teks_prediksi = "TIDAK HUJAN (CERAH/BERAWAN) ☀️"
        pesan_saran = "Cuaca mendukung untuk aktivitas luar ruangan."

    return {
        "status": "success",
        "prediksi": teks_prediksi,
        "probabilitas_hujan": round(probabilitas * 100, 2),
        "pesan": pesan_saran
    }

# Code di bawah agar bisa dirun langsung dengan `python api_weather.py`
if __name__ == "__main__":
    # Host 0.0.0.0 agar bisa diakses dari Nginx, Port 8000 sesuai config Nginx tadi
    uvicorn.run("api_weather:app", host="0.0.0.0", port=8000, reload=True)