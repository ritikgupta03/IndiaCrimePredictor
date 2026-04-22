import json

def inspect_candidate(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"File: {filepath}")
        print(f"Feature count: {len(data['features'])}")
        
        if len(data['features']) > 0:
            feat = data['features'][0]
            print(f"Properties example: {feat.get('properties', {}).keys()}")
            # Print unique state names if available
            names = set()
            for f in data['features']:
                p = f['properties']
                for k in ['name', 'ST_NM', 'NAME_1', 'State']:
                    if k in p: names.add(p[k])
            print(f"Names found ({len(names)}): {list(names)[:10]}...")
            
    except Exception as e:
        print(f"Error: {e}")

inspect_candidate('candidate_1.json')
