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
            # Check common name keys in Highcharts format (usually 'name' or 'hc-key')
            name = props.get('name') or props.get('hc-key')
            if name:
                names.add(name)
        
        print("State Names identified:")
        for name in sorted(list(names)):
            print(f"- {name}")
            
    except Exception as e:
        print(f"Error: {e}")

audit_geojson('static/data/india_highcharts.json')
