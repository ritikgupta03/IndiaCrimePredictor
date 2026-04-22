import requests
try:
    res = requests.get('http://127.0.0.1:5000/api/predict')
    data = res.json()
    print("Multi-year Forecast (2026-2028):")
    for year, count in data.items():
        print(f"Year {year}: {count:,}")
except Exception as e:
    print(f"Error: {e}")
