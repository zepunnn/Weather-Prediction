import pandas as pd
from app.models.model_loader import CURRENT_MODEL

def test_model_predictions():
    if CURRENT_MODEL is None:
        print("[ERROR] Model belum di load. Jalankan server FastAPI atau retrain model.")
        return
    
    skenario = [
        [32, 60, 10, 12], #Tidak Hujan (Pagi/Siang)
        [24, 95, 5, 17], #Lembap atau Berawan (Sore)
        [27, 85, 20, 20], # Malam
    ]

    df_test = pd.DataFrame(skenario, columns=["temperature", "humidity", "wind_speed", "jam"])
    hasil = CURRENT_MODEL.predict(df_test)
    prob = CURRENT_MODEL.predict_proba(df_test)

    print("\n=== TESTING PREDIKSI MODEL ===")
    for i, h in enumerate(hasil):
        kondisi = "HUJAN" if h == 1 else "TIDAK HUJAN"
        keyakinan = prob[i][h] * 100

        print(f"\nKasus {i+1}:")
        print(f"  Input     : {skenario[i]}")
        print(f"  Prediksi  : {kondisi}")
        print(f"  Keyakinan : {keyakinan:.2f}%")