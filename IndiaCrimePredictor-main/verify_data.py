import pandas as pd
import os

csv_path = r'c:\Users\rohit\Downloads\crime\dataset\india_crime_data_cleaned.csv'
df = pd.read_csv(csv_path)

print(f"Total rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

# Check for "Total" rows
total_rows = df[df.apply(lambda row: row.astype(str).str.contains('Total', case=False).any(), axis=1)]
print(f"Rows containing 'Total': {len(total_rows)}")
if len(total_rows) > 0:
    print(total_rows.head(10))

# Check unique categories
print(f"Unique Categories: {df['Crime Category'].unique()}")

# Check UP 2025 sum
up_2025 = df[(df['State/UT'] == 'Uttar Pradesh') & (df['Year'] == 2025)]
print(f"UP 2025 Sum of 'Number of Cases': {up_2025['Number of Cases'].sum()}")

# Check if there are rows where District is 'Total'
dist_totals = df[df['District'].str.contains('Total', case=False, na=False)]
print(f"Rows where District contains 'Total': {len(dist_totals)}")
