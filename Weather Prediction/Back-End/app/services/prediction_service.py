from app.models.model_loader import CURRENT_MODEL
import pandas as pd

def predict_weather_service(data: dict):
    """
    Menerima dictionary data input dan menghasilkan:
    - prediksi
    - probability
    - message """

    if CURRENT_MODEL is None:
        return None
    
    df_input = pd.DataFrame([{
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "wind_speed": data["wind_speed"],
        "jam": data["jam"],
    }])

    #predict
    hasil = CURRENT_MODEL.predict(df_input)[0]
    probabilitas = CURRENT_MODEL.predict_proba(df_input)[0][1]

    if hasil == 1:
        prediksi = "HUJAN"
        message = "Harap untuk mempersiapkan diri terhadap cuaca hujan."
    else:
        prediksi = "TIDAK HUJAN"
        message = "Cuaca sedang cerah."
    
    return {
        "prediksi": prediksi,
        "probability": round(probabilitas * 100, 2),
        "message": message
    }