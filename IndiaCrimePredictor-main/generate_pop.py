import pandas as pd
import numpy as np
import os

# Base 2011 Population (Simplified approx in millions)
pop_2011 = {
    "Uttar Pradesh": 199.8, "Maharashtra": 112.4, "Bihar": 104.1, "West Bengal": 91.3,
    "Madhya Pradesh": 72.6, "Tamil Nadu": 72.1, "Rajasthan": 68.5, "Karnataka": 61.1,
    "Gujarat": 60.4, "Andhra Pradesh": 49.3, "Odisha": 41.9, "Telangana": 35.1,
    "Kerala": 33.4, "Jharkhand": 33.0, "Assam": 31.2, "Punjab": 27.7,
    "Chhattisgarh": 25.5, "Haryana": 25.3, "Delhi": 16.8, "Jammu & Kashmir": 12.2,
    "Uttarakhand": 10.1, "Himachal Pradesh": 6.8, "Tripura": 3.6, "Meghalaya": 2.9,
    "Manipur": 2.8, "Nagaland": 1.9, "Goa": 1.4, "Arunachal Pradesh": 1.3,
    "Puducherry": 1.2, "Mizoram": 1.0, "Chandigarh": 1.0, "Sikkim": 0.6,
    "Andaman & Nicobar Islands": 0.38, "Dadra & Nagar Haveli and Daman & Diu": 0.58,
    "Lakshadweep": 0.06, "Ladakh": 0.27
}

# Projected Growth Rates (Annualized approx %)
growth_rates = {
    "UP": 1.5, "Bihar": 1.8, "Kerala": 0.5, "Tamil Nadu": 0.7, "National": 1.1
}

years = list(range(2014, 2029))
data = []

for state, base_pop in pop_2011.items():
    current_pop = base_pop * (1.011 ** 3) # Approx 2014 start from 2011
    for year in years:
        # Vary growth slightly by region
        rate = 0.012 if state in ["Bihar", "Uttar Pradesh", "Rajasthan"] else (0.006 if state in ["Kerala", "Tamil Nadu"] else 0.01)
        data.append({"State/UT": state, "Year": year, "Population": int(current_pop * 1_000_000)})
        current_pop *= (1 + rate)

pop_df = pd.DataFrame(data)
os.makedirs('dataset', exist_ok=True)
pop_df.to_csv('dataset/india_population_2014_2028.csv', index=False)
print("Population dataset generated: dataset/india_population_2014_2028.csv")
