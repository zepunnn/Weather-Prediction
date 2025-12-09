import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

DATA_PATH = "dataset/weather_data.csv"
MODEL_SAVE_PATH = "saved_model.pkl"

def train_offline():

    print("[TRAINING] Memuat dataset...")
    df = pd.read_csv(DATA_PATH)

    df['datetime_local'] = pd.to_datetime(df['datetime_local'])
    df['jam'] = df['datetime_local'].dt.hour
    df['is_raining'] = df['weather_desc'].str.contains("hujan|rain", case=False).astype(int)

    X = df[['temperature', 'humidity', 'wind_speed', 'jam']]
    y = df['is_raining']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)

    print(f"[TRAINING] Akurasi model: {acc * 100:.2f}%")

    with open(MODEL_SAVE_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"[MODEL] Model disimpan ke {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train_offline()