from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.model_loader import load_or_train_model
from app.routers import prediction

app = FastAPI(
    title="API Prediksi Cuaca BMKG",
    description=""Backend Machine Learning untuk Prediksi Cuaca",
    version="1.0"
)

#Global Model
MODEL = None
MODEL_ACCURACY = 0.0

# CORS SETUP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#STARTUP EVENT
def startup_event():
    global MODEL, MODEL_ACCURACY
    MODEL, MODEL_ACCURACY = load_or_train_model()
    print("[SYSTEM] Model siap dipakai.")

#ROUTING
app.include_router(prediction.router)

#HOME
@app.get("/")
def home():
    return {
        "message": "API Prediksi Cuaca Online",
        "model_status": "Ready" if MODEL else "Not Ready",
        "model_accuracy": f"{MODEL_ACCURACY * 100:.2f}%"
    }