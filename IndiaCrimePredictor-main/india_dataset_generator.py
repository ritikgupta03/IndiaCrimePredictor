import pandas as pd
import numpy as np
import os
import requests

def generate_scaled_india_data():
    print("🚀 Initializing High-Volume India Crime Dataset Generator (500k+ records)...")
    
    # States & UTs (36)
    states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", 
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", 
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", 
        "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman & Nicobar Islands", 
        "Chandigarh", "Dadra & Nagar Haveli and Daman & Diu", "Delhi", "Jammu & Kashmir", 
        "Ladakh", "Lakshadweep", "Puducherry"
    ]
    
    # Comprehensive Crime Categories (NCRB Style)
    categories = [
        "Murder", "Attempt to Murder", "Culpable Homicide", "Rape", "Kidnapping & Abduction",
        "Robbery", "Burglary", "Theft", "Riots", "Dowry Deaths", "Cruelty by Husband",
        "Assault on Women", "Sexual Harassment", "Cyber Crimes", "Cheating", "Forgery",
        "Counterfeiting", "Arson", "Grievous Hurt", "Extortion", "Possession of Drugs",
        "Human Trafficking", "Child Abuse", "Financial Fraud", "Corruption Cases"
    ]
    
    # Years (11 Year Trend)
    years = list(range(2014, 2026)) 
    
    # Simulate Districts (Avg 50 per state for ~500k records)
    districts_per_state = 50
    
    data = []
    
    # Population/Crime Weightage
    state_weights = {
        "Uttar Pradesh": 10.0, "Maharashtra": 8.5, "Bihar": 7.5, "West Bengal": 7.0,
        "Madhya Pradesh": 6.5, "Tamil Nadu": 6.0, "Rajasthan": 6.0, "Karnataka": 5.5,
        "Gujarat": 5.0, "Delhi": 5.5, "Kerala": 3.0, "Goa": 0.5, "Sikkim": 0.2, "Ladakh": 0.1
    }

    # Generate records
    print(f"Generating data for {len(states)} States, ~{len(states)*districts_per_state} Districts, over {len(years)} years...")
    
    for state in states:
        weight = state_weights.get(state, 2.5)
        for d_idx in range(districts_per_state):
            district_name = f"{state}_Dist_{d_idx+1}"
            dist_base_risk = np.random.uniform(0.5, 1.5)
            
            for category in categories:
                cat_base = np.random.randint(5, 50) if weight < 3 else np.random.randint(50, 500)
                
                for year in years:
                    trend = 1 + (year - 2014) * np.random.uniform(0.02, 0.08)
                    cases = int(cat_base * weight * dist_base_risk * trend * np.random.uniform(0.8, 1.2))
                    
                    data.append({
                        "State/UT": state, "District": district_name, "Crime Category": category,
                        "Year": year, "Number of Cases": cases
                    })
                    
    df = pd.DataFrame(data)
    
    # --- ENHANCED DATA AUGMENTATION ---
    print("🚀 Applying Synthetic Data Augmentation & Feature Engineering...")
    
    # 1. Ensure realistic increasing trend at high level
    # We add a small annual boost to ensure it doesn't drop off
    df['Number of Cases'] = df.apply(lambda row: int(row['Number of Cases'] * (1 + (row['Year'] - 2014) * 0.02)), axis=1)

    # 2. Create Lag Features & Rolling Averages
    df = df.sort_values(['District', 'Crime Category', 'Year'])
    df['Lag_1'] = df.groupby(['District', 'Crime Category'])['Number of Cases'].shift(1)
    df['Lag_2'] = df.groupby(['District', 'Crime Category'])['Number of Cases'].shift(2)
    df['Rolling_3yr_Avg'] = df.groupby(['District', 'Crime Category'])['Number of Cases'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    
    # 3. Growth Rate (Previous Year)
    df['Growth_Rate'] = ((df['Number of Cases'] - df['Lag_1']) / df['Lag_1'].replace(0, 1) * 100).fillna(0)
    df['Growth_Rate'] = df['Growth_Rate'].clip(-50, 200) # Keep it realistic
    
    os.makedirs('dataset', exist_ok=True)
    raw_path = 'dataset/india_crime_data.csv'
    df.to_csv(raw_path, index=False)
    
    # Cleaning Pipeline
    print("🧹 Running Data Cleaning & Normalization Pipeline...")
    df_cleaned = df.dropna(subset=['Lag_1']).copy() # Drop first year for model stability
    
    # Capping outliers to avoid extreme spikes in models
    upper_limit = df_cleaned['Number of Cases'].quantile(0.999)
    df_cleaned['Number of Cases'] = df_cleaned['Number of Cases'].clip(0, upper_limit)
    
    cleaned_path = 'dataset/india_crime_data_cleaned.csv'
    df_cleaned.to_csv(cleaned_path, index=False)
    
    print(f"✅ Success! Generated {len(df)} records.")
    print(f"Cleaned/Augmented dataset saved to {cleaned_path}")

if __name__ == "__main__":
    generate_scaled_india_data()
