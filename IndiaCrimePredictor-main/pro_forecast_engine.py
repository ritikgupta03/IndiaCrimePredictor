import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def train_pro_models():
    print("Initializing Professional Forecasting Engine...")
    df = pd.read_csv('dataset/india_crime_data_cleaned.csv')
    
    # Preprocess categorical data
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df['State_Encoded'] = le.fit_transform(df['State/UT'])
    
    # Feature Engineering
    states = df['State/UT'].unique()
    featured_data = []
    
    for state in states:
        s_df = df[df['State/UT'] == state].sort_values('Year')
        s_df['Lag_1'] = s_df['Number of Cases'].shift(1)
        s_df['Lag_2'] = s_df['Number of Cases'].shift(2)
        s_df['Rolling_3yr'] = s_df['Number of Cases'].rolling(window=3).mean()
        # Safe growth rate
        s_df['Growth_Rate'] = s_df['Number of Cases'].pct_change().replace([np.inf, -np.inf], 0).fillna(0)
        s_df['Growth_Rate'] = s_df['Growth_Rate'].clip(-1, 5) # Cap growth at 500%
        featured_data.append(s_df)
    
    df_feat = pd.concat(featured_data)
    
    # Strict Cleaning
    df_feat = df_feat.replace([np.inf, -np.inf], np.nan)
    initial_len = len(df_feat)
    df_feat = df_feat.dropna(subset=['Number of Cases', 'Year', 'Lag_1', 'Lag_2', 'Rolling_3yr', 'Growth_Rate'])
    print(f"Data Cleaning: Removed {initial_len - len(df_feat)} malformed rows.")

    if len(df_feat) < 10:
        print("ERROR: Insufficient data after cleaning.")
        return

    X = df_feat[['Year', 'State_Encoded', 'Lag_1', 'Lag_2', 'Rolling_3yr', 'Growth_Rate']]
    y = df_feat['Number of Cases']
    
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.15, random_state=42)
    
    # 1. Baseline: Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_mae = mean_absolute_error(y_test, lr_pred)
    
    # 2. Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    
    # 3. XGBoost Quantile Regression (For Confidence Intervals)
    # Note: objective='reg:quantileerror' might not be available in older XGB versions
    # We will try absoluteerror as fallback or just use MAE
    xgb_params = {'n_estimators': 100, 'learning_rate': 0.1, 'max_depth': 5}
    xgb_median = XGBRegressor(**xgb_params)
    xgb_median.fit(X_train, y_train)
    xgb_mae = mean_absolute_error(y_test, xgb_median.predict(X_test))
    
    # Simple Interval Logic if Quantile not fully supported by local env
    try:
        xgb_upper = XGBRegressor(objective='reg:quantileerror', quantile_alpha=0.95, **xgb_params)
        xgb_upper.fit(X_train, y_train)
        xgb_lower = XGBRegressor(objective='reg:quantileerror', quantile_alpha=0.05, **xgb_params)
        xgb_lower.fit(X_train, y_train)
    except:
        print("Falling back to absolute error for intervals...")
        xgb_upper = XGBRegressor(**xgb_params)
        xgb_upper.fit(X_train, y_train * 1.2) # Crude fallback
        xgb_lower = XGBRegressor(**xgb_params)
        xgb_lower.fit(X_train, y_train * 0.8) # Crude fallback

    print(f"Model Calibration -> LR MAE: {lr_mae:.2f}, RF MAE: {rf_mae:.2f}, XGB MAE: {xgb_mae:.2f}")
    
    # Selection
    os.makedirs('models/pro', exist_ok=True)
    joblib.dump(xgb_median, 'models/pro/model_median.joblib')
    joblib.dump(xgb_upper, 'models/pro/model_upper.joblib')
    joblib.dump(xgb_lower, 'models/pro/model_lower.joblib')
    joblib.dump(le, 'models/pro/state_le.joblib')
    joblib.dump(scaler, 'models/pro/scaler.joblib')
    joblib.dump({'mae': xgb_mae, 'r2': r2_score(y_test, xgb_median.predict(X_test))}, 'models/pro/metrics.joblib')
    
    print("Professional models saved to models/pro/")

if __name__ == "__main__":
    train_pro_models()
