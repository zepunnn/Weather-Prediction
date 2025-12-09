# 🌦️ Beather: Weather Prediction Project for Batang, Central Java, Indonesia

![Project Status](https://img.shields.io/badge/Status-On--Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Machine Learning](https://img.shields.io/badge/AI-Scikit--Learn-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> **Delivering hyper-local weather intelligence for Batang, Central Java — powered by Machine Learning and real-time BMKG Open Data.**

---

## 📖 Overview

**Beather (Batang Weather)**—also known internally as **BatangCast**—is a weather prediction platform built to deliver accurate, ML-driven forecasts for the **Batang Regency** region.

Unlike generic applications that only provide city-level weather information, Beather focuses on **Kelurahan/Desa-level predictions**, enabling a far more precise and actionable forecast for residents, farmers, fishermen, and daily commuters.

This system transforms complex meteorological datasets from **BMKG** into meaningful predictions through an automated pipeline, from data ingestion to prediction serving.

---

## ✨ Key Features

* **📍 Hyper-Local Forecasting:** View predictions filtered down to specific **Kelurahan/Desa** within Batang Regency.
* **🤖 AI-Powered Predictions:** Machine Learning models identify rainfall likelihood and weather patterns using historical BMKG data.
* **📊 Interactive Visualization:** Dynamic, user-friendly charts (Chart.js) for understanding weather trends.
* **⚡ Fast & Modern API:** Backend built with **FastAPI**, offering high performance and async capability.
* **🎨 TypeScript Frontend:** A modern and responsive interface built with TypeScript for safer, scalable, and maintainable code.
* **🔄 Automated ETL Pipeline:** Continuous synchronization with BMKG Open Data to keep the system up to date.

---

## 🏗️ Tech Stack

This project uses a **decoupled architecture** to ensure scalability, clean data flow, and maintainability.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend & API** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **FastAPI** | Handles requests, serves ML predictions, manages preprocessing. |
| **Machine Learning** | **Pandas & Scikit-Learn** | Data pipeline, feature extraction, model training & evaluation. |
| **Database** | ![MySQL](https://img.shields.io/badge/MySQL-005C84?style=flat&logo=mysql&logoColor=white) **MySQL** | Stores historical BMKG weather data and prediction logs. |
| **Frontend** | ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white) **TypeScript** | Modern, typed UI for displaying weather predictions and graphs. |
| **Visualization** | **Chart.js** | Renders interactive charts for temperature, rainfall, and trends. |

---

## 📁 Project Folder Structure
beather/
│
├── app/ # Backend (FastAPI)
│ ├── main.py # API entry point
│ ├── database.py # MySQL connection
│ ├── routers/
│ │ └── prediction.py # Weather prediction API routes
│ ├── services/
│ │ └── prediction_service.py
│ ├── models/
│ │ ├── model_loader.py # Load/train ML model
│ │ └── ml_model.pkl # Saved ML model
│ ├── schemas/
│ │ └── prediction_schema.py
│ └── utils/
│ ├── import_data.py # Fetch BMKG Open Data
│ └── preprocessing.py # Data cleaning helpers
│
├── ml_model/ # Offline ML workspace
│ ├── train_model.ipynb # Notebook for experimentation
│ ├── training_script.py # Offline training
│ ├── export_dataset.py # Export DB → CSV
│ └── dataset/
│ └── weather_data.csv # Raw dataset
│
├── database/
│ ├── schema.sql # MySQL table definitions
│ └── seed.sql # Optional sample data
│
├── frontend/ # TypeScript Web App
│ ├── src/
│ │ ├── index.ts # Main TS entry
│ │ ├── components/
│ │ ├── pages/
│ │ └── services/
│ └── package.json
│
└── README.md
A clean, scalable architecture separating backend, machine learning assets, and the TypeScript frontend.


---

## 🗺️ System Architecture Diagram

A high-level overview of Beather’s architecture:

                    ┌───────────────────────────┐
                    │      BMKG Open Data        │
                    └──────────────┬─────────────┘
                                   │
                    (1) Fetch & Ingest via import_data.py
                                   │
            ┌──────────────────────▼──────────────────────┐
            │                  MySQL DB                   │
            │ (weather_log: temp, humidity, wind, rain)   │
            └──────────────┬──────────────────────────────┘
                           │
     (2) Export / (3) Train Model (Automatic or Offline)
                           │
            ┌──────────────▼──────────────────────┐
            │          ML Model (pkl)             │
            │ RandomForestClassifier / Regressor  │
            └──────────────┬──────────────────────┘
                           │
                 (4) FastAPI Backend
                           │
            ┌──────────────▼──────────────────────┐
            │         Prediction API               │
            │   /predict?adm4_code=xxxx            │
            └──────────────┬──────────────────────┘
                           │
                 (5) JSON Response
                           │
          ┌────────────────▼─────────────────┐
          │        TypeScript Frontend        │
          │ Chart.js Graphs, UI Visuals       │
          └───────────────────────────────────┘

---

## 🚀 How It Works

1. **Data Ingestion:** BMKG Open Data is fetched and stored into the MySQL database via automated scripts.
2. **Data Processing:** Backend scripts preprocess and clean the dataset for ML training.
3. **Prediction Serving:** When a user selects a *Kelurahan*, FastAPI loads the trained model and performs inference.
4. **Result Presentation:** The API returns weather predictions, visualized instantly on the TypeScript frontend.

---

## 🧠 Model & Dataset

* **Dataset Source:** [BMKG Open Data](https://data.bmkg.go.id/)
* **Features:** Temperature, Humidity, Wind Speed, Rainfall Indicators.
* **Model Types:**  
  * **Rain Classification** — RandomForestClassifier  
  * **General Weather Trend** — RandomForestRegressor  
* **Training Workflow:** Periodically retrained using accumulated BMKG historical data.

---

## 🤝 Contributing

Contributions are welcome!  
Developers, data enthusiasts, or anyone passionate about weather modeling in Indonesia are encouraged to fork this repository and submit Pull Requests.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

---

<p align="center">
  Made with ❤️ for <b>Batang, Central Java, Indonesia</b>
</p>
