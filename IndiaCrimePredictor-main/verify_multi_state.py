import requests
states = ["Maharashtra", "Delhi", "Kerala", "Bihar"]
for state in states:
    try:
        res = requests.get(f'http://127.0.0.1:5000/api/state_analysis?state={state}&year=2025')
        data = res.json()
        print(f"State: {state} | Growth: {data['predicted_growth_rate']}% | Forecast: {data['forecast']}")
    except:
        print(f"Error for {state}")
