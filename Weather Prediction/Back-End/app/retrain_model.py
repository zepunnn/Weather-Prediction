from app.models.model_loader import train_model

def retrain():
    print("\n=== RETRAIN MODEL ===")
    model, acc = train_model()

    if model is None:
        print("[FAILED] Model gagal ditraining.")
    else:
        print(f"[SUCCESS] Model baru tersimpan. Akurasi: {acc*100:.2f}%")

if_name_ == "__main__":
    retrain()