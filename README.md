<div align="center">
  <h1>🚔 India Crime Predictor AI</h1>
  <p><b>An Advanced Machine Learning-based Crime Analysis & Forecasting System</b></p>
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-lightgrey.svg?style=for-the-badge&logo=flask" alt="Flask" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg?style=for-the-badge&logo=scikit-learn" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/License-MIT-success.svg?style=for-the-badge" alt="License" />
</div>

<br>

## 📌 Overview

**India Crime Predictor AI** is an intelligent, full-stack data analytics and forecasting platform. Built with Python and Flask, it processes historical crime data across Indian states and union territories to uncover hidden patterns, visualize insights via interactive maps, and predict future crime trends using robust Machine Learning models.

Unlike a simple dashboard, this platform provides **automated anomaly detection**, **risk categorization**, and **predictive modeling** to assist law enforcement agencies, policymakers, and researchers in making data-driven decisions.

---

## ✨ Key Features

- **📊 Comprehensive Data Analytics:** State-wise and district-level crime insights filtered by IPC and SLL categories.
- **🗺️ Interactive Geo-Spatial Maps:** Dynamic mapping and heatmaps to visualize high-risk zones and crime concentration.
- **🤖 Predictive Forecasting:** Time-series forecasting using linear regression and advanced statistical modeling to predict future crime volumes.
- **⚡ Real-time Anomaly Detection:** Instantly identifies statistical anomalies in crime rates for proactive intervention.
- **📑 Automated PDF Reports:** One-click generation of professional "Intelligence & Risk Reports" for immediate sharing.
- **🌐 Dynamic Web Interface:** A fast, responsive, and intuitive web application powered by Flask.

---

## 🛠️ Technology Stack

| Category | Technologies |
| --- | --- |
| **Backend Framework** | Flask, Python |
| **Machine Learning** | Scikit-Learn, XGBoost, Numpy |
| **Data Processing** | Pandas |
| **Visualization** | Matplotlib, Seaborn, Plotly, Folium |
| **Report Generation** | ReportLab |
| **Deployment Prep** | Gunicorn (WSGI), Vercel Configuration |

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.8+ installed on your system.

### 1. Installation
Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/your-username/IndiaCrimePredictor.git
cd IndiaCrimePredictor

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 📡 API Endpoints Overview

The application exposes several RESTful APIs used by the frontend for dynamic updates:

- `GET /api/stats` - Fetches high-level KPIs, top states, and national forecasts.
- `GET /api/state_analysis` - Retrieves deep-dive historical data, risk levels, and forecasts for a specific state.
- `GET /api/predict` - Generates multi-year predictive trends globally or categorically.
- `GET /api/export/pdf` - Generates and downloads a comprehensive PDF intelligence report.
- `GET /api/export/csv` - Downloads the processed and cleaned dataset as a CSV file.

---

## ☁️ Deployment

This project is fully prepared for cloud deployment. 

### Option 1: Render / Heroku (Recommended)
The project includes a `Procfile` and `gunicorn` in the requirements. 
1. Push your code to GitHub.
2. Link your repository in the **Render** dashboard.
3. Render will automatically install dependencies and launch the app using `gunicorn app:app`.

### Option 2: Vercel
A `vercel.json` file is included for Vercel deployment. 
*Note: Vercel serverless functions have a strict 250MB size limit. Due to the size of ML libraries and datasets, deploying on Render is highly recommended over Vercel.*

---

## 📂 Project Structure

```text
IndiaCrimePredictor/
├── app.py                   # Main Flask Application & API Routes
├── forecasting_utils.py     # ML forecasting, risk & anomaly logic
├── dataset/                 # Crime & Population Datasets (CSV)
├── static/                  # CSS, JS, and Images for the frontend
├── templates/               # HTML templates (Jinja2)
├── Procfile                 # Deployment configuration for Render/Heroku
├── vercel.json              # Deployment configuration for Vercel
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚠️ Limitations & Disclaimers
- **Data Dependency:** Forecast accuracy is strictly dependent on the quality of historical data.
- **Not a Replacement:** Predictions are statistical estimates and should be used to augment, not replace, human operational intelligence.

---

## 🔮 Future Enhancements
- Integration of live API feeds from NCRB (National Crime Records Bureau).
- Implementation of Deep Learning (LSTM) for complex time-series pattern recognition.
- Dedicated mobile application dashboard for on-field officers.

---

<div align="center">
  <p><b>Built with ❤️ for Data-Driven Governance</b></p>
  <p>MIT License © 2026</p>
</div>
