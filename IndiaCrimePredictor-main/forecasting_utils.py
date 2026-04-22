import pandas as pd
import numpy as np
import joblib
import os
from sklearn.linear_model import LinearRegression

# Load Core Data
BASE_DF = pd.read_csv('dataset/india_crime_data.csv')
POP_DF = pd.read_csv('dataset/india_population_2014_2028.csv')

def get_anomaly_status(state, year):
    """Safe statistical anomaly detection"""
    try:
        state_df = BASE_DF[BASE_DF['State/UT'] == state].sort_values('Year')
        if len(state_df) < 3: return False
        
        vals = state_df.groupby('Year')['Number of Cases'].sum().values
        mean, std = np.mean(vals), np.std(vals)
        curr = state_df[state_df['Year'] == year]['Number of Cases'].sum()
        
        return bool(curr > mean + 2*std)
    except Exception:
        return False

def calculate_per_capita(count, state, year):
    """Normalize count to per 100k population"""
    try:
        pop_row = POP_DF[(POP_DF['State/UT'] == state) & (POP_DF['Year'] == year)]
        if not pop_row.empty:
            population = pop_row['Population'].iloc[0]
            return round((count / population) * 100000, 2)
        return 0
    except Exception:
        return 0

def generate_safe_forecast(state, year, horizon=3):
    """Simple Linear Regression Forecast as requested for stability"""
    try:
        state_df = BASE_DF[BASE_DF['State/UT'] == state].groupby('Year')['Number of Cases'].sum().reset_index()
        state_df = state_df.sort_values('Year')
        
        if len(state_df) < 3: return []
        
        X = state_df['Year'].values.reshape(-1, 1)
        y = state_df['Number of Cases'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        results = []
        for i in range(1, horizon + 1):
            target_year = year + i
            pred = int(model.predict([[target_year]])[0])
            # Ensure no negative predictions
            pred = max(0, pred)
            
            results.append({
                "year": int(target_year),
                "yhat": pred,
                "upper": int(pred * 1.1), # Simplified CI
                "lower": int(pred * 0.9)  # Simplified CI
            })
        return results
    except Exception as e:
        print(f"Safe Forecast Error: {e}")
        return []

def get_state_risk(state, year, use_per_capita=False):
    """Categorize risk based on quantiles for the given year"""
    try:
        yearly_df = BASE_DF[BASE_DF['Year'] == year].copy()
        
        state_data = yearly_df.groupby('State/UT')['Number of Cases'].sum()
        
        if use_per_capita:
            # Map population
            merged = yearly_df.merge(POP_DF[POP_DF['Year'] == year][['State/UT', 'Population']], on='State/UT')
            merged['rate'] = (merged['Number of Cases'] / merged['Population']) * 100000
            state_data = merged.groupby('State/UT')['rate'].sum()
            
        q_low = state_data.quantile(0.33)
        q_high = state_data.quantile(0.66)
        
        val = state_data.get(state, 0)
        
        if val >= q_high: return "High"
        elif val >= q_low: return "Medium"
        return "Low"
    except Exception:
        return "Low"
