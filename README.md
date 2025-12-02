# 🌦️ BatangCast: Hyper-Local Weather Foresight

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Machine Learning](https://img.shields.io/badge/AI-Scikit--Learn-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> **Empowering the citizens of Batang, Central Java, with precision weather insights down to the village (Kelurahan) level.**

---

## 📖 Overview

**BatangCast** is a web-based application designed to provide accurate weather predictions for the **Batang Regency** area. Unlike generic weather apps that only show data for the city center, BatangCast utilizes **Machine Learning** to analyze historical open data from **BMKG** (Indonesian Agency for Meteorology, Climatology, and Geophysics) to predict weather conditions specific to local sub-districts and villages.

This project bridges the gap between complex meteorological data and the daily needs of the local community—helping farmers, fishermen, and commuters prepare for the day ahead.

## ✨ Key Features

* **📍 Hyper-Local Granularity:** Filter weather predictions specifically by **Kelurahan/Desa** within Batang Regency.
* **🤖 AI-Powered Predictions:** Uses advanced regression and classification models to forecast rainfall and temperature trends.
* **📊 Interactive Visualization:** Beautiful charts and graphs (powered by Chart.js) to visualize weather patterns easily.
* **⚡ Lightweight Web Interface:** A fast and responsive Frontend accessible from any device (Mobile/Desktop).
* **🔄 Real-time Data Pipeline:** Automated integration with BMKG Open Data.

## 🏗️ Tech Stack

This project implements a **Decoupled Architecture**, separating the heavy data processing from the user interface.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend & AI** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Flask** | Handles API requests, runs ML models, and processes data. |
| **Machine Learning** | **Pandas & Scikit-Learn** | Data cleaning, feature engineering, and predictive modeling. |
| **Database** | ![MySQL](https://img.shields.io/badge/MySQL-005C84?style=flat&logo=mysql&logoColor=white) **MySQL** | Stores historical weather data and prediction logs (Hosted on Ubuntu). |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | User interface for selecting locations and viewing graphs. |
| **Visualization** | **Chart.js** | Renders dynamic weather charts on the client side. |

## 🚀 How It Works

1.  **Data Ingestion:** The system fetches open weather data from BMKG stations around Central Java.
2.  **Processing:** Python scripts clean the data and store it in the **MySQL** database on an Ubuntu server.
3.  **Prediction:** When a user selects a *Kelurahan*, the backend runs the ML model against historical patterns for that specific topography.
4.  **Presentation:** The API sends JSON data to the Frontend, where it is rendered into easy-to-read cards and graphs.

## 🛠️ Installation & Setup

If you want to run this project locally:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/batang-weather-forecast.git](https://github.com/yourusername/batang-weather-forecast.git)
    cd batang-weather-forecast
    ```

2.  **Set up the Environment**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Database**
    * Import the provided `database_schema.sql` to your local MySQL.
    * Update `config.py` with your database credentials.

4.  **Run the Server**
    ```bash
    python app.py
    ```

5.  **Open in Browser**
    Visit `http://localhost:5000`

## 🧠 Model & Dataset

* **Dataset Source:** [BMKG Open Data](https://data.bmkg.go.id/)
* **Parameters:** Humidity, Temperature, Wind Speed, and Rainfall (Curah Hujan).
* **Algorithm:** Random Forest Regressor & Logistic Regression (for rain classification).

## 🤝 Contributing

Contributions are welcome! If you are a developer from Batang or interested in weather data, feel free to fork this repository and submit a Pull Request.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Made with ❤️ for <b>Batang, Indonesia</b>
</p>
