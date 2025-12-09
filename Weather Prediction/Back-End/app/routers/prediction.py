from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from app.models.model_loader import CURRENT_MODEL, MODEL_ACCURACY

router = APIRouter(prefix="/predict", tags=["Prediction"])

#Schema Input
class WeatherInput(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    jam: int

#Schema Output
class PredictionResponse(BaseModel):
    status: str
    prediksi: str
    probability: float
    message: str

#Endpoint
@router.post("/", response_model=PredictionResponse)
def predict_weather(data: WeatherInput):
    
    if CURRENT_MODEL is None:
        raise HTTPException(status_code=503, detail="Model belum siap.")
    
    #Input harus sesuai urutan training
    df_input = pd.DataFrame([{
        "temperature": data.temperature,
        "humidity": data.humidity,
        "wind_speed": data.wind_speed,
        "jam": data.jam
    }])

    hasil = CURRENT_MODEL.predict(df_input)[0]
    probabilitas = CURRENT_MODEL.predict_proba(df_input)[0][1]

    if hasil == 1:
        prediksi = "HUJAN"
        message = "Harap untuk mempersiapkan diri terhadap cuaca hujan."
    else:
        prediksi = "TIDAK HUJAN"
        message = "Cuaca sedang cerah."
    
    return {
        "status": "success",
        "prediksi": prediksi,
        "probability": probabilitas,
        "message": message
    }