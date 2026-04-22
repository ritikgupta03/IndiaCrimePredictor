import requests
try:
    res = requests.get('http://127.0.0.1:5000/api/stats?year=2025')
    data = res.json()
    print(f"Total Crimes 2025: {data['kpis']['total_crimes']}")
    print(f"Forecast 2026: {data['kpis']['forecast']}")
except Exception as e:
    print(f"Error: {e}")
