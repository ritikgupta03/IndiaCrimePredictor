import json

def audit_geojson(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"File: {filepath}")
        print(f"Feature count: {len(data['features'])}")
        
        names = set()
        for feature in data['features']:
            props = feature['properties']
            # Check common name keys
            for key in ['name', 'ST_NM', 'NAME_1', 'State_Name']:
                if key in props:
                    names.add(props[key])
        
        print("State Names identified:")
        for name in sorted(list(names)):
            print(f"- {name}")
            
    except Exception as e:
        print(f"Error: {e}")

audit_geojson('static/data/india_states.json')
