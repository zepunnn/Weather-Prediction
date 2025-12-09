import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from app.database import get_connection

MODEL_PATH = "app/models/ml_model.pkl"

CURRENT_MODEL = None
MODEL_ACCURACY = 0.0

#Train Model dari Database
def train_model():
    print("[MODEL] Training model dari database...")

    conn = get_connection()
    if conn is None:
        print("[MODEL] Gagal connect.")
        return None, 0.0
    
    query = """
    SELECT datetime_local, temperature, humidity, wind_speed, weather_desc
    FROM weather_log
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if len(df) < 10:
        print("[MODEL] Data terlalu sedikit untuk training.")
        return None, 0.0
    
    #Feature Engineering
    df["datetime_local"] = pd.to_datetime(df["datetime_local"])
    df["jam"] = df["datetime_local"].dt.hour
    df["is_raining"] = df["weather_desc"].apply(lamda x: 1 if "hujan" in x.lower() or "rain" in x.lower() else 0)

    x = df[["temperature", "humidity", "wind_speed", "jam"]]
    y = df["is_raining"]

    #Train Test Split
    if len(x) >= 10:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    else:
        x_train, x_test, y_train, y_test = x, x, y, y

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    prediction = model.predict(x_test)
    accuracy = accuracy_score(y_test, prediction)

    print(f"[MODEL] Training selesai. Akurasi: {accuracy:.2f}%")

    #Save Model
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    
    return model, accuracy

#Load Model
def load_model_from_file():
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                return pickle.load(f)
        except:
            return None
    return None

#Load or Train Model
def load_or_train_model():
    global CURRENT_MODEL, MODEL_ACCURACY

    model = load_model_from_file()
    if model:
        print("[MODEL] Model berhasil di load.")
        CURRENT_MODEL = model
        MODEL_ACCURACY = 0.0
        return model, MODEL_ACCURACY
    
    model, accuracy = train_model()
    CURRENT_MODEL = model
    MODEL_ACCURACY = accuracy
    return model, accuracy