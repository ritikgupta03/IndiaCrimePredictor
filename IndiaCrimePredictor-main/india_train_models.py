import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
import joblib
import os

def train_advanced_models():
    print("📂 Loading Cleaned High-Volume Crime Dataset...")
    df = pd.read_csv('dataset/india_crime_data_cleaned.csv')
    
    os.makedirs('models', exist_ok=True)
    
    # 1. Feature Engineering: Temporal Lags & Trends
    print("🛠️ Engineering Temporal Features (Lags & Rolling Averages)...")
    df = df.sort_values(['District', 'Crime Category', 'Year'])
    
    # Lags: Cases from previous 1 and 2 years
    df['Lag_1'] = df.groupby(['District', 'Crime Category'])['Number of Cases'].shift(1)
    df['Lag_2'] = df.groupby(['District', 'Crime Category'])['Number of Cases'].shift(2)
    
    # Drop rows without lags for training
    df_ml = df.dropna(subset=['Lag_1', 'Lag_2']).copy()
    
    # Encode Categories
    le_state = LabelEncoder()
    le_cat = LabelEncoder()
    df_ml['State_Encoded'] = le_state.fit_transform(df_ml['State/UT'])
    df_ml['Category_Encoded'] = le_cat.fit_transform(df_ml['Crime Category'])
    
    # 2. Advanced Forecasting Model (XGBoost)
    print("🤖 Training Advanced Temporal Forecasting Model (XGBoost)...")
    # Features: Year, State, Category, Prev Year, 2022 Year, Rolling Trend
    features = ['Year', 'State_Encoded', 'Category_Encoded', 'Lag_1', 'Lag_2', 'Rolling_3yr_Avg']
    X = df_ml[features]
    y = df_ml['Number of Cases']
    
    model_forecast = xgb.XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        objective='reg:squarederror',
        n_jobs=-1
    )
    model_forecast.fit(X, y)
    
    joblib.dump(model_forecast, 'models/advanced_forecast_model.joblib')
    joblib.dump(le_state, 'models/state_label_encoder.joblib')
    joblib.dump(le_cat, 'models/category_label_encoder.joblib')
    
    # 3. Enhanced Risk Profiling (KMeans on Temporal Trends)
    print("📊 Training Multivariate Risk Profiling (KMeans)...")
    state_metrics = df.groupby('State/UT').agg({
        'Number of Cases': 'mean',
        'Growth_Rate': 'mean',
        'Rolling_3yr_Avg': 'mean'
    }).reset_index()
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(state_metrics[['Number of Cases', 'Growth_Rate', 'Rolling_3yr_Avg']])
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    state_metrics['Risk_Cluster'] = kmeans.fit_predict(scaled_data)
    
    # Map clusters to Low/Medium/High
    cluster_means = state_metrics.groupby('Risk_Cluster')['Number of Cases'].mean().sort_values()
    risk_mapping = {
        cluster_means.index[0]: "Low",
        cluster_means.index[1]: "Medium",
        cluster_means.index[2]: "High"
    }
    
    state_risk_dict = {row['State/UT']: risk_mapping[row['Risk_Cluster']] for _, row in state_metrics.iterrows()}
    joblib.dump(state_risk_dict, 'models/state_risk_mapping.joblib')
    
    print("✅ Advanced Models Trained and Saved!")

if __name__ == "__main__":
    train_advanced_models()
