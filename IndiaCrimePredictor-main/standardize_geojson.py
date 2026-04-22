import json

def standardize_geojson(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Mapping to match the dataset exactly
    mapping = {
        "Andaman and Nicobar Islands": "Andaman & Nicobar Islands",
        "Dadra and Nagar Haveli and Daman and Diu": "Dadra & Nagar Haveli and Daman & Diu",
        "Jammu and Kashmir": "Jammu & Kashmir"
    }
    
    for feature in data['features']:
        name = feature['properties'].get('name')
        if name in mapping:
            feature['properties']['name'] = mapping[name]
            print(f"Renamed: {name} -> {mapping[name]}")
            
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    print(f"Standardized GeoJSON saved to {output_path}")

standardize_geojson('static/data/india_highcharts.json', 'static/data/india_states_v2.json')
standardize_geojson('static/data/india_highcharts.json', 'static/data/india_states.json') # Directly overwrite for immediate fix
