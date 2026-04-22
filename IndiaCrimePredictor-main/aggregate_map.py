import json
from collections import defaultdict

def aggregate_to_states(districts_path, output_path):
    with open(districts_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    state_polygons = defaultdict(list)
    
    # Normalization Map
    norm_map = {
        "Andaman and Nicobar": "Andaman & Nicobar Islands",
        "Andaman & Nicobar": "Andaman & Nicobar Islands",
        "Dadra and Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu",
        "Daman and Diu": "Dadra & Nagar Haveli and Daman & Diu",
        "Dadra & Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu",
        "Jammu and Kashmir": "Jammu & Kashmir",
        "Orissa": "Odisha",
        "Uttaranchal": "Uttarakhand",
        "NCT of Delhi": "Delhi",
        "Pondicherry": "Puducherry"
    }

    for feature in data['features']:
        full_name = feature['properties'].get('FULL_NAME', '')
        if ',' in full_name:
            state = full_name.split(',')[-1].strip()
        else:
            state = full_name
        
        # TitleCase and standardized separators
        state = state.title().replace(' And ', ' & ')
        if state.endswith(' And'): state = state[:-4] + ' &' # Handle 'And' at end
        
        norm_map = {
            "Andaman & Nicobar Islands": "Andaman & Nicobar Islands",
            "Andaman And Nicobar Islands": "Andaman & Nicobar Islands",
            "Himachal Pradesh": "Himachal Pradesh",
            "Madhya Pradesh": "Madhya Pradesh",
            "Arunachal Pradesh": "Arunachal Pradesh",
            "Uttar Pradesh": "Uttar Pradesh",
            "Dadra & Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu",
            "Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu",
            "Dadra & Nagar Haveli & Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu",
            "Jammu & Kashmir": "Jammu & Kashmir",
            "Nct Of Delhi": "Delhi",
            "Delhi": "Delhi",
            "Orissa": "Odisha",
            "Pondicherry": "Puducherry"
        }
        
        normalized_state = norm_map.get(state, state)
        state_polygons[normalized_state].append(feature['geometry'])

    # Create State Features
    state_features = []
    for state, geometries in state_polygons.items():
        # We'll use MultiPolygon to hold all geometries for a state
        combined_coords = []
        for g in geometries:
            if g['type'] == 'Polygon':
                combined_coords.append(g['coordinates'])
            elif g['type'] == 'MultiPolygon':
                combined_coords.extend(g['coordinates'])
        
        state_features.append({
            "type": "Feature",
            "properties": {"name": state, "ST_NM": state},
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": combined_coords
            }
        })

    new_geojson = {
        "type": "FeatureCollection",
        "features": state_features
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_geojson, f)
    print(f"Created clean state map: {output_path} with {len(state_features)} states.")

aggregate_to_states('static/data/india_districts_simplified.json', 'static/data/india_states.json')
