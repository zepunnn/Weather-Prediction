import pandas as pd

def add_time_features(df: pd.DataFrame):
    """Menambahkan fitur jam dari kolom datetime_local."""
    df["datetime_local"] = pd.to_datetime(df["datetime_local"])
    df["jam"] = df["datetime_local"].dt.hour
    return df

def add_rain_label(df: pd.DataFrame):
    """Menambahkan kolom is_raining berdasarkan weather_desc"""
    df["is_raining"] = df["weather_desc"].apply(
        lambda x: 1 if "hujan" in x.lower() or "rain" in x.lower() else 0
    )
    return df

def prepare_features(df: pd.DataFrame):
    """Membuat dataset siap masuk model (x dan y)"""
    df = add_time_features(df)
    df = add_rain_label(df)

    x = df[["temperature", "humidity", "wind_speed", "jam"]]
    y = df["is_raining"]

    return x, y
