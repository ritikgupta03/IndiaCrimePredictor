import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import joblib
import os

def train_best_forecast_model():
    print("Loading Augmented India Crime Dataset...")
    df = pd.read_csv('dataset/india_crime_data_cleaned.csv')
    
    # 1. Proper Aggregation: National Yearly Totals
    # The primary forecast should be based on the national trend
    print("Aggregating National Yearly Totals for Trend Analysis...")
    national_yearly = df.groupby('Year').agg({
        'Number of Cases': 'sum',
        'Rolling_3yr_Avg': 'sum'
    }).reset_index()
    
    # Add Lag features at national level for better time-series fit
    national_yearly['Lag_1'] = national_yearly['Number of Cases'].shift(1)
    national_yearly['Lag_2'] = national_yearly['Number of Cases'].shift(2)
    national_yearly = national_yearly.dropna()
    
    # 2. Prepare Features
    # We use Year, Lag_1, Lag_2, and Rolling_3yr_Avg
    features = ['Year', 'Lag_1', 'Lag_2', 'Rolling_3yr_Avg']
    X = national_yearly[features]
    y = national_yearly['Number of Cases']
    
    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"Training and Comparing Models using {len(national_yearly)} years of aggregated data...")
    
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost": xgb.XGBRegressor(n_estimators=100, objective='reg:squarederror')
    }
    
    best_model = None
    best_r2 = -float('inf')
    best_name = ""
    
    results = []
    
    for name, model in models.items():
        model.fit(X_scaled, y)
        preds = model.predict(X_scaled)
        
        rmse = np.sqrt(mean_squared_error(y, preds))
        mae = mean_absolute_error(y, preds)
        r2 = r2_score(y, preds)
        
        results.append({
            "Model": name,
            "RMSE": round(rmse, 2),
            "MAE": round(mae, 2),
            "R2": round(r2, 4)
        })
        
        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_name = name
            
    # Display Results
    print(f"Best Model Selected: {best_name} (R2: {best_r2:.4f})")
    
    # 3. Save Best Model and Scaler
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_model, 'models/best_forecast_model.joblib')
    joblib.dump(scaler, 'models/forecast_scaler.joblib')
    joblib.dump(best_name, 'models/best_model_name.joblib')
    
    # Also save the latest national totals for smoothing logic in backend
    national_yearly.to_csv('models/latest_national_trend.csv', index=False)
    print("Best Model and metadata saved to 'models/'")

if __name__ == "__main__":
    train_best_forecast_model()
