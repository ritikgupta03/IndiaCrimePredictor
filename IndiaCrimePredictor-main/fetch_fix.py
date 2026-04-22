import requests
import json

urls = {
    "JK": "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d117038/raw/c559885e7839655866a1e367878939678120e8b2/jk.json",
    "Ladakh": "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d117038/raw/c559885e7839655866a1e367878939678120e8b2/ladakh.json"
}

for name, url in urls.items():
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            # Max Lat
            max_lat = -90
            def get_m(c):
                m = -90
                for x in c:
                    if isinstance(x[0], list): m = max(m, get_m(x))
                    else: m = max(m, float(x[1]))
                return m
            
            # GeoJSON can be Feature or FeatureCollection
            if data.get('type') == 'Feature':
                max_lat = get_m(data['geometry']['coordinates'])
            else:
                for f in data.get('features', []):
                    max_lat = max(max_lat, get_m(f['geometry']['coordinates']))
            
            print(f"{name}: Max Lat {max_lat}")
            with open(f"{name}_fix.json", 'w') as f:
                json.dump(data, f)
        else:
            print(f"Failed {name}: {r.status_code}")
    except Exception as e:
        print(f"Error {name}: {e}")
