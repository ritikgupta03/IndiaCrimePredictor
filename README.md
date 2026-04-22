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

🚀 https://india-crime-predictor.onrender.com/

---

## 📌 Overview

India Crime Predictor AI is a full-stack data analytics and forecasting system that analyzes historical crime data across India to generate insights, detect anomalies, and predict future crime trends.

The platform combines machine learning, data processing, and visualization to support decision-making for analysis and research purposes.

---

## ✨ Key Features

- 📊 State-wise and district-level crime analytics  
- 🗺️ Interactive geo-spatial heatmaps  
- 🤖 Time-series crime prediction using ML models  
- ⚡ Anomaly detection system  
- 📑 Automated PDF report generation  
- 🌐 Dynamic Flask-based web interface  

---

## 🧠 Workflow

```text
Data Collection
      ↓
Data Cleaning
      ↓
Model Training
      ↓
Prediction
      ↓
Visualization
      ↓
Report Generation
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|---------|-------------|
| Backend | Flask, Python |
| Machine Learning | Scikit-Learn, XGBoost |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Plotly, Folium |
| Reporting | ReportLab |
| Deployment | Gunicorn, Render |

---

## 📡 API Endpoints

- `GET /api/stats`  
- `GET /api/state_analysis`  
- `GET /api/predict`  
- `GET /api/export/pdf`  
- `GET /api/export/csv`  

---

## 🚀 Getting Started

### 🔧 Installation

```bash
git clone https://github.com/your-username/IndiaCrimePredictor.git
cd IndiaCrimePredictor

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### ▶️ Run Project
```bash
python app.py
```
Open: `http://127.0.0.1:5000`

---

## ☁️ Deployment

### Render (Live)
Command: `gunicorn app:app`

**Steps:**
1. Push code to GitHub
2. Connect to Render
3. Deploy

---

## 📂 Project Structure
```text
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
```

---

## ⚠️ Limitations
- Depends on dataset quality
- Predictions are statistical estimates
- Not a real-time law enforcement system

---

## 🔮 Future Scope
- NCRB API integration
- Deep Learning (LSTM)
- Mobile application
- Real-time monitoring

---

## 👨‍💻 Project Team
- Ritik Gupta
- Rohit Madhesiya
- Riya Kumari

---

## 📜 License

MIT License © 2026

<div align="center"> 
  <h3>🚀 Built for Data Analysis & Research</h3> 
</div>
