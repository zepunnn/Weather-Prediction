-- ==========================================
--  DATABASE SCHEMA UNTUK PREDIKSI CUACA BMKG
-- ==========================================

CREATE DATABASE IF NOT EXISTS bmkg_data;
USE bmkg_data;

-- ===============================
--  TABEL LOG CUACA (DATA HISTORIS)
-- ===============================
CREATE TABLE IF NOT EXISTS weather_log (
    id INT AUTO_INCREMENT PRIMARY KEY,

    adm4_code VARCHAR(20) NOT NULL,
    datetime_local DATETIME NOT NULL,

    temperature FLOAT DEFAULT NULL,
    humidity INT DEFAULT NULL,
    wind_speed FLOAT DEFAULT NULL,

    weather_desc VARCHAR(255) DEFAULT "-",

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY unique_weather (adm4_code, datetime_local)
);

-- INDEX tambahan untuk mempercepat query
CREATE INDEX idx_datetime ON weather_log(datetime_local);
CREATE INDEX idx_adm4 ON weather_log(adm4_code);
CREATE INDEX idx_israin ON weather_log(weather_desc);