import json

def extract_northern_points(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    northern_points = []
    # Candidate 1 is a single feature or FeatureCollection
    features = data['features'] if 'features' in data else [data]
    
    for feature in features:
        geom = feature['geometry']
        coords = geom['coordinates']
        
        def process_coords(c):
            pts = []
            for x in c:
                if isinstance(x[0], list):
                    pts.extend(process_coords(x))
                else:
                    if float(x[1]) > 34.5: # Include some margin
                        pts.append(x)
            return pts
        
        northern_points.extend(process_coords(coords))
    
    # Sort northern points by longitude to make a chain
    northern_points.sort(key=lambda x: x[0])
    
    print(f"Total points > 34.5: {len(northern_points)}")
    if northern_points:
        print(f"Sample: {northern_points[:5]}")
        print(f"Max Lat Found: {max(p[1] for p in northern_points)}")

extract_northern_points('candidate_1.json')
