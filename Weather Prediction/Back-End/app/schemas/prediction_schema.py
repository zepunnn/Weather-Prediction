from pydantic import BaseModel

class WeatherInput(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    jam: int

class PredictionResponse(BaseModel):
    status: str
    prediksi: str
    probabilitas: float
    message: str