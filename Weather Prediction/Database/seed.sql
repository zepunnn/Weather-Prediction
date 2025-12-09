USE bmkg_data;

INSERT INTO weather_log (adm4_code, datetime_local, temperature, humidity, wind_speed, weather_desc)
VALUES
    ("33.25.11.1015", "2025-01-01 12:00:00", 32.5, 60, 10, "Cerah"),
    ("33.25.11.1015", "2025-01-01 15:00:00", 29.0, 85, 5, "Hujan Ringan"),
    ("33.25.11.1015", "2025-01-01 18:00:00", 27.0, 95, 7, "Hujan Lebat"),
    ("33.25.11.1015", "2025-01-02 09:00:00", 30.0, 70, 4, "Berawan"),
    ("33.25.11.1015", "2025-01-02 16:00:00", 25.0, 90, 6, "Hujan Sedang");