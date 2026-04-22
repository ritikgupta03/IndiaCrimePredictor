import pandas as pd

df = pd.read_csv(r'c:\Users\rohit\Downloads\crime\dataset\india_crime_data_cleaned.csv')
haryana_2021 = df[(df['State/UT'] == 'Haryana') & (df['Year'] == 2021)].copy()

# Remove Total rows as per my logic
haryana_2021 = haryana_2021[
    ~haryana_2021['State/UT'].str.contains('Total', case=False, na=False) &
    ~haryana_2021['District'].str.contains('Total', case=False, na=False) &
    ~haryana_2021['Crime Category'].str.contains('Total', case=False, na=False)
]

print(f"Haryana 2021 Rows: {len(haryana_2021)}")
category_sum = haryana_2021.groupby('Crime Category')['Number of Cases'].sum().sort_values(ascending=False)
print("Category Breakdown:")
print(category_sum)

total_ipc_sum = category_sum.sum()
print(f"Total Sum: {total_ipc_sum}")

print("\nDistrict Count for Murder:")
murder_dist = haryana_2021[haryana_2021['Crime Category'] == 'Murder']
print(murder_dist.groupby('District')['Number of Cases'].count())
