<div align="center">
  <h1>🚔 India Crime Predictor AI</h1>
  <p><b>AI-Powered Crime Analytics & Forecasting Platform</b></p>

  <img src="https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Flask-Backend-lightgrey.svg?style=for-the-badge&logo=flask"/>
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg?style=for-the-badge&logo=scikit-learn"/>
  <img src="https://img.shields.io/badge/Status-Live-success?style=for-the-badge"/>
</div>

---

## 🌐 Live Demo

🚀 **Deployed Application:**  
👉 https://india-crime-predictor.onrender.com/

> Fully functional cloud-hosted ML system accessible in real-time.

---

## 📌 Overview

**India Crime Predictor AI** is a full-stack intelligent analytics and forecasting system that analyzes historical crime data across India to generate insights, detect anomalies, and predict future crime trends.

The platform combines **Machine Learning, Data Analytics, and Visualization** to support:

- 👮 Law Enforcement Agencies  
- 🏛️ Policymakers  
- 📊 Researchers  

---

## ✨ Key Features

- 📊 State-wise & district-level crime analytics  
- 🗺️ Interactive geo-spatial heatmaps  
- 🤖 Time-series crime prediction (ML models)  
- ⚡ Anomaly detection system  
- 📑 Automated PDF report generation  
- 🌐 Dynamic Flask-based web interface  

---

## 🧠 Machine Learning Workflow


Data Collection (CSV)
↓
Data Cleaning (Pandas)
↓
Feature Engineering
↓
Model Training (Linear Regression / XGBoost)
↓
Prediction
↓
Visualization (Charts + Maps)
↓
PDF Report Generation


---

## 🛠️ Tech Stack

| Category | Technologies |
|---------|-------------|
| Backend | Flask, Python |
| ML | Scikit-Learn, XGBoost |
| Data | Pandas, NumPy |
| Visualization | Matplotlib, Plotly, Folium |
| Reports | ReportLab |
| Deployment | Gunicorn, Render |

---

## 📡 API Endpoints

- `GET /api/stats` → National insights  
- `GET /api/state_analysis` → State data  
- `GET /api/predict` → Forecast predictions  
- `GET /api/export/pdf` → Download report  
- `GET /api/export/csv` → Export dataset  

---

## 🚀 Getting Started

### 🔧 Installation

```bash
git clone https://github.com/your-username/IndiaCrimePredictor.git
cd IndiaCrimePredictor

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
▶️ Run Project
python app.py

👉 Open: http://127.0.0.1:5000

☁️ Deployment
✅ Render (Live)

Project deployed using:

gunicorn app:app

Steps:

Push code to GitHub
Connect to Render
Auto deploy
📂 Project Structure
IndiaCrimePredictor/
├── app.py
├── forecasting_utils.py
├── dataset/
├── static/
├── templates/
├── Procfile
├── vercel.json
├── requirements.txt
└── README.md
⚠️ Limitations
Accuracy depends on dataset quality
Predictions are statistical estimates
Not a replacement for real policing systems
🔮 Future Scope
NCRB Live API Integration
LSTM Deep Learning Model
Mobile Application
Real-time monitoring system
👨‍💻 Project Team
🚀 Developed By

Ritik Gupta
Full Stack Developer & ML Engineer

Rohit Madhesiya
Backend Developer

Riya Kumari
Frontend Developer

🤝 Contributions
Ritik Gupta
ML Model & Prediction System
Backend API Development
Rohit Madhesiya
Data Processing & Backend Logic
Riya Kumari
UI/UX Design & Frontend
📜 License

MIT License © 2026

<div align="center"> <h3>🚀 Built for Data-Driven Governance</h3> </div> ```
