import requests
import json

try:
    # Test for Uttar Pradesh in 2025
    res = requests.get('http://127.0.0.1:5000/api/state_analysis?state=Uttar%20Pradesh&year=2025')
    data = res.json()
    print(f"State: {data['state']}")
    print(f"Current Cases (2025): {data['selected_year_cases']:,}")
    print(f"Forecast: {data['forecast']}")
    print(f"Predicted Growth: {data['predicted_growth_rate']}%")
    print(f"Trend: {data['predicted_trend']}")
    
    # Check if forecast year is 2026
    if "2026" in data['forecast'] or 2026 in data['forecast']:
        print("✅ Forecast year is 2026")
    else:
        print("❌ Forecast year is NOT 2026")
        
except Exception as e:
    print(f"Error: {e}")
