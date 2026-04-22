import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def train_state_forecast_model():
    print("Loading India Crime Dataset for State Training...")
    df = pd.read_csv('dataset/india_crime_data_cleaned.csv')
    
    # 1. State-Year Aggregation
    print("Aggregating Data by State and Year...")
    state_yearly = df.groupby(['State/UT', 'Year']).agg({
        'Number of Cases': 'sum',
        'Rolling_3yr_Avg': 'sum',
        'Growth_Rate': 'mean'
    }).reset_index()
    
    # Add Lags at State Level
    state_yearly = state_yearly.sort_values(['State/UT', 'Year'])
    state_yearly['Lag_1'] = state_yearly.groupby('State/UT')['Number of Cases'].shift(1)
    state_yearly['Lag_2'] = state_yearly.groupby('State/UT')['Number of Cases'].shift(2)
    state_yearly = state_yearly.dropna()
    
    # 2. Encoding State Names
    le_state = LabelEncoder()
    state_yearly['State_Encoded'] = le_state.fit_transform(state_yearly['State/UT'])
    
    # 3. Prepare Features
    # Features: Year, State_Encoded, Lag_1, Lag_2, Rolling_3yr_Avg, Growth_Rate
    features = ['Year', 'State_Encoded', 'Lag_1', 'Lag_2', 'Rolling_3yr_Avg', 'Growth_Rate']
    X = state_yearly[features]
    y = state_yearly['Number of Cases']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"Training State-Aware XGBoost Model on {len(state_yearly)} state-year records...")
    
    model = xgb.XGBRegressor(
        n_estimators=2000, 
        learning_rate=0.03, 
        max_depth=8, 
        subsample=0.8,
        colsample_bytree=0.8,
        objective='reg:squarederror',
        random_state=42
    )
    
    model.fit(X_scaled, y)
    
    # Evaluation
    preds = model.predict(X_scaled)
    r2 = r2_score(y, preds)
    print(f"State Model Training Complete. R2 Score: {r2:.4f}")
    
    # 4. Save Artifacts
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/state_forecast_model.joblib')
    joblib.dump(scaler, 'models/state_scaler.joblib')
    joblib.dump(le_state, 'models/state_label_encoder.joblib')
    
    print("State-Aware Model artifacts saved to 'models/'")

if __name__ == "__main__":
    train_state_forecast_model()
