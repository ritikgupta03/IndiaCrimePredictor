🚔 CrimePredictAI – AI Crime Analysis & Forecasting System

A powerful Machine Learning-based crime analysis platform built with Python & Flask, designed to uncover patterns, visualize insights, and predict future crime trends.

📌 Overview

CrimePredictAI is not just a data analysis tool — it’s a complete intelligent system that combines:

📊 Data Analytics
🤖 Machine Learning
🗺️ Geo-Spatial Visualization
🌐 Web Application

to deliver real-world crime insights and forecasting capabilities.

✨ Features
📊 Smart Data Analysis
Crime category-wise, state & district-level insights
🗺️ Interactive Maps
GeoJSON-based visualization with heatmaps
🤖 ML Forecasting
Time-series prediction for future crime trends
⚙️ Model Optimization
Automatic best model selection pipeline
🌐 Flask Web App
Dynamic UI with real-time rendering
📈 Forecast Engine
Multi-state predictive analytics
💡 Recommendations
Data-driven crime prevention suggestions
🛠️ Tech Stack
Core: Python
Framework: Flask
ML Libraries: Scikit-learn
Data Handling: Pandas, NumPy
Visualization: Matplotlib, GeoJSON
📂 Project Structure
crime1/
 ├── crime/
 │   ├── app.py              # Flask entry point
 │   ├── dataset/
 │   ├── models/
 │   ├── templates/
 │   ├── static/
 │
 │   ├── india_train_models.py
 │   ├── train_best_model.py
 │   ├── train_state_model.py
 │
 │   ├── forecasting_utils.py
 │   ├── pro_forecast_engine.py
 │
 │   ├── recommendations.py
 │
 │   ├── aggregate_map.py
 │   ├── stitch_map.py
 │   ├── audit_geojson.py
 │
 │   ├── verify_*.py
 │   └── requirements.txt
🧠 Key Technical Highlights
✔ Separation of Concerns (UI, logic, data separated)
✔ Predictive Modeling using ML
✔ Modular & scalable architecture
✔ Clean and validated datasets
✔ Geo-based analysis
⚠️ Limitations
Depends heavily on dataset quality
Prediction may vary for unseen data
Requires properly formatted GeoJSON
🔮 Future Enhancements
Real-time crime data integration
Deep learning models (LSTM, RNN)
Mobile application
AI-based alert system


📜 License

MIT License © 2026
