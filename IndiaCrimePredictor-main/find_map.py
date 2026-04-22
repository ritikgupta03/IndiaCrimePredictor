import requests
import json
import os

urls = [
    "https://raw.githubusercontent.com/Anuj6142/India-map-GeoJSON/master/india_states.json",
    "https://raw.githubusercontent.com/datameet/maps/master/States/Admin1.json",
    "https://raw.githubusercontent.com/shubhamsandhu/india-geojson/master/india_states.json",
    "https://raw.githubusercontent.com/subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States.json"
]

results = []

for url in urls:
    try:
        print(f"Trying {url}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(url, timeout=10, headers=headers)
        print(f"Final URL: {r.url}, Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            # Calculate max latitude
            max_lat = -90
            for feat in data.get('features', []):
                geom = feat.get('geometry', {})
                if not geom: continue
                coords = geom.get('coordinates', [])
                
                def get_max_lat(c):
                    m = -90
                    for x in c:
                        if isinstance(x[0], list):
                            m = max(m, get_max_lat(x))
                        else:
                            m = max(m, float(x[1]))
                    return m
                
                max_lat = max(max_lat, get_max_lat(coords))
            
            results.append({"url": url, "max_lat": max_lat, "size": len(r.content)})
            print(f"SUCCESS: Max Lat: {max_lat}, Size: {len(r.content)}")
            
            # Save if it seems high enough (> 36 degrees)
            if max_lat > 36.5:
                fname = f"candidate_{len(results)}.json"
                with open(fname, 'w') as f:
                    json.dump(data, f)
                print(f"Saved to {fname}")
        else:
            print(f"Failed with status: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

print("\n--- Summary ---")
for res in results:
    print(res)
